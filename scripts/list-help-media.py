#!/usr/bin/env python3
"""
Generate a filename checklist for whoever's capturing screenshots and
short videos for the StemCounts help site.

Output: docs/HELP_MEDIA_CHECKLIST.md (overwritten on each run).

The checklist is the *capture* side of the workflow:

    1. Kate (or whoever) opens this list + app.stemcounts.com side by side.
    2. For each item, she captures the screenshot or short video.
    3. She saves it with the exact filename from this list.
    4. She drops all the captured files into one folder.
    5. Someone with AWS access uploads that folder's contents into the
       help-media.stemcounts.com S3 bucket (flat at root, no folders).

The list is grouped by article so the capture work happens in a
natural sequence. Each filename sits in its own fenced code block, so
GitHub renders a copy icon on each one — click, paste into Save-as,
done.

Run from repo root any time articles change:

    python scripts/list-help-media.py
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "src" / "content" / "docs"
OUT = REPO_ROOT / "docs" / "HELP_MEDIA_CHECKLIST.md"

BUCKET_NAME = "help-media.stemcounts.com"

TAG_RE = re.compile(
    r"<HelpMedia\b([^/>]*?)\bid\s*=\s*\"([^\"]+)\"([^/>]*)/?>",
    re.MULTILINE,
)
ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')


@dataclass
class Reference:
    slug: str
    kind: str
    caption: str | None
    article_url: str
    article_title: str


def parse_attrs(*chunks: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for chunk in chunks:
        for m in ATTR_RE.finditer(chunk):
            attrs[m.group(1)] = m.group(2)
    return attrs


def article_title(mdx: Path) -> str:
    text = mdx.read_text(encoding="utf-8")
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return mdx.stem
    fm = m.group(1)
    title_m = re.search(r"^title:\s*(.+)$", fm, re.MULTILINE)
    if title_m:
        return title_m.group(1).strip().strip('"').strip("'")
    return mdx.stem


def article_url(mdx: Path) -> str:
    rel = mdx.relative_to(DOCS).as_posix().replace(".mdx", "")
    if rel.endswith("/index"):
        rel = rel[: -len("/index")]
    if rel == "index":
        rel = ""
    return ("/" + rel + "/").replace("//", "/")


SECTION_ORDER = ["getting-started", "florists", "wholesalers", "billing", "faqs", "changelog"]


def section_of(path: str) -> str:
    rel = path.lstrip("/")
    if not rel:
        return ""
    return rel.split("/", 1)[0]


def main() -> None:
    references: list[Reference] = []
    for mdx in sorted(DOCS.rglob("*.mdx")):
        text = mdx.read_text(encoding="utf-8")
        title = article_title(mdx)
        url = article_url(mdx)
        for m in TAG_RE.finditer(text):
            pre, slug, post = m.group(1), m.group(2), m.group(3)
            attrs = parse_attrs(pre, post)
            references.append(
                Reference(
                    slug=slug,
                    kind=attrs.get("kind", "image"),
                    caption=attrs.get("caption"),
                    article_url=url,
                    article_title=title,
                )
            )

    by_article: dict[str, list[Reference]] = defaultdict(list)
    for ref in references:
        by_article[ref.article_url].append(ref)

    unique_slugs = {r.slug for r in references}
    video_slugs = {r.slug for r in references if r.kind == "video"}
    image_count = len(unique_slugs) - len(video_slugs)

    lines: list[str] = []
    lines.append("# Help-media filename checklist")
    lines.append("")
    lines.append(
        f"A list of every screenshot and short video the StemCounts help "
        f"site is set up for. **{len(unique_slugs)} files in total** — "
        f"{image_count} screenshots + {len(video_slugs)} short videos."
    )
    lines.append("")

    # ── For the capturer (Kate) ───────────────────────────────────────
    lines.append("## How to use this list")
    lines.append("")
    lines.append("1. Open this page and <https://app.stemcounts.com> side by side.")
    lines.append("2. Work through the list below, article by article.")
    lines.append("3. For each entry, capture the screenshot or short video the description points at.")
    lines.append("4. Save it with the **exact filename** in the code block — click the copy icon on the code block and paste it into your Save-as dialog.")
    lines.append("5. Drop everything you capture into one folder on your desktop.")
    lines.append("6. Hand the folder over — uploading is somebody else's job (see the bottom of this page).")
    lines.append("")
    lines.append("Don't rename files, add prefixes, or change extensions. The filenames in this list are the links the help site already expects — get them wrong and the image won't appear.")
    lines.append("")
    lines.append("### Capture guidelines")
    lines.append("")
    lines.append("- **Screenshots**: capture at 2× (Retina) for crispness; aim for roughly 2400px wide max.")
    lines.append("- **Short videos**: MP4 (H.264), 1080p max, under 30 seconds where possible, ideally under 20 MB.")
    lines.append("- **Redact**: blur or replace real florist names, customer names, real prices, and addresses before saving.")
    lines.append("")
    lines.append("Click any article title to open the live page so you can see exactly where the image will sit.")
    lines.append("")

    # ── Per-article list ──────────────────────────────────────────────
    lines.append("## Files to capture, by article")
    lines.append("")

    def article_sort_key(url: str) -> tuple[int, str]:
        sec = section_of(url)
        try:
            order = SECTION_ORDER.index(sec)
        except ValueError:
            order = len(SECTION_ORDER)
        return (order, url)

    for url in sorted(by_article.keys(), key=article_sort_key):
        refs = by_article[url]
        title = refs[0].article_title
        lines.append(f"### [{title}]({url})")
        lines.append("")

        seen_slugs: dict[str, Reference] = {}
        for ref in refs:
            seen_slugs.setdefault(ref.slug, ref)

        for slug, ref in seen_slugs.items():
            ext = "mp4" if ref.kind == "video" else "png"
            filename = f"{slug}.{ext}"
            kind_tag = "🎥 **short video**" if ref.kind == "video" else "📷 screenshot"

            lines.append(f"- [ ] {kind_tag}")
            lines.append("")
            lines.append("  ```")
            lines.append(f"  {filename}")
            lines.append("  ```")
            lines.append("")
            if ref.caption:
                lines.append(f"  *Show:* {ref.caption}")
                lines.append("")

        lines.append("")

    # ── Alphabetical lookup ───────────────────────────────────────────
    lines.append("---")
    lines.append("")
    lines.append("## Quick alphabetical lookup")
    lines.append("")
    lines.append("If you need to find a specific filename fast:")
    lines.append("")
    for slug in sorted(unique_slugs):
        ref_for_slug = next(r for r in references if r.slug == slug)
        ext = "mp4" if ref_for_slug.kind == "video" else "png"
        lines.append(f"- `{slug}.{ext}` → [{ref_for_slug.article_title}]({ref_for_slug.article_url})")

    # ── Uploader section (separate, not for Kate) ─────────────────────
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## For whoever's uploading the folder")
    lines.append("")
    lines.append("Files go into a single S3 bucket, at the root level — no folders.")
    lines.append("")
    lines.append("**Bucket name:**")
    lines.append("")
    lines.append("```")
    lines.append(BUCKET_NAME)
    lines.append("```")
    lines.append("")
    lines.append("Steps:")
    lines.append("")
    lines.append("1. AWS Console → S3 → click into `help-media.stemcounts.com`.")
    lines.append("2. **Upload** → drag the captured-files folder contents in (not the folder itself — just the loose files).")
    lines.append("3. Leave the default options, click **Upload** at the bottom.")
    lines.append("4. Trigger a docs site rebuild in Amplify (or wait — they'll appear on the next push to `main`).")
    lines.append("")
    lines.append("If a file's filename doesn't match a slug, it'll sit silently in the bucket without showing up on the help site. Match the list above exactly.")
    lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"Wrote {OUT.relative_to(REPO_ROOT)} — "
        f"{len(unique_slugs)} files "
        f"({image_count} screenshots, {len(video_slugs)} videos) "
        f"across {len(by_article)} articles."
    )


if __name__ == "__main__":
    main()
