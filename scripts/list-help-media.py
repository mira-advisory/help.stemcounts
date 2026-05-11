#!/usr/bin/env python3
"""
Generate a markdown checklist of every <HelpMedia> slug referenced in
articles, so whoever is capturing screenshots / video walkthroughs can
work through it methodically.

Output: docs/HELP_MEDIA_CHECKLIST.md (overwritten on each run).

Grouped by article (the natural unit of work — capture everything for
one article in one sitting), with each filename rendered as a
copy-friendly code block. GitHub adds a copy button to fenced code
blocks automatically.

Run from repo root:

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

# Match <HelpMedia ...id="slug"... />, capturing surrounding attributes.
TAG_RE = re.compile(
    r"<HelpMedia\b([^/>]*?)\bid\s*=\s*\"([^\"]+)\"([^/>]*)/?>",
    re.MULTILINE,
)
ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')


@dataclass
class Reference:
    slug: str
    kind: str  # "image" or "video"
    caption: str | None
    article_path: str  # filesystem path within docs
    article_url: str
    article_title: str


def parse_attrs(*chunks: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for chunk in chunks:
        for m in ATTR_RE.finditer(chunk):
            attrs[m.group(1)] = m.group(2)
    return attrs


def article_title(mdx: Path) -> str:
    """Pull the `title:` field from the frontmatter so the checklist
    shows article names (not slugs) for context."""
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
    """Convert the on-disk path to the live URL on help.stemcounts.com."""
    rel = mdx.relative_to(DOCS).as_posix().replace(".mdx", "")
    if rel.endswith("/index"):
        rel = rel[: -len("/index")]
    if rel == "index":
        rel = ""
    return ("/" + rel + "/").replace("//", "/")


# Section ordering for the output (matches sidebar order in astro.config.mjs).
SECTION_ORDER = ["getting-started", "florists", "wholesalers", "billing", "faqs", "changelog"]


def section_of(path: str) -> str:
    """First path segment — used for grouping output by section."""
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
            kind = attrs.get("kind", "image")
            caption = attrs.get("caption")
            references.append(
                Reference(
                    slug=slug,
                    kind=kind,
                    caption=caption,
                    article_path=str(mdx),
                    article_url=url,
                    article_title=title,
                )
            )

    # Group by article URL so capture work happens article-by-article.
    by_article: dict[str, list[Reference]] = defaultdict(list)
    for ref in references:
        by_article[ref.article_url].append(ref)

    # Counts for the summary.
    unique_slugs = {r.slug for r in references}
    video_slugs = {r.slug for r in references if r.kind == "video"}
    image_count = len(unique_slugs) - len(video_slugs)

    # Build output.
    lines: list[str] = []
    lines.append("# Help-media upload checklist")
    lines.append("")
    lines.append(
        f"Every `<HelpMedia>` reference across the StemCounts help site, listed by "
        f"article. **{len(unique_slugs)} files total** — {image_count} images + "
        f"{len(video_slugs)} short videos."
    )
    lines.append("")

    # ── Top instructions ──────────────────────────────────────────────
    lines.append("## How to upload")
    lines.append("")
    lines.append("Every file goes into one S3 bucket, at the root level — no folders.")
    lines.append("")
    lines.append("**Bucket name:**")
    lines.append("")
    lines.append("```")
    lines.append(BUCKET_NAME)
    lines.append("```")
    lines.append("")
    lines.append("### Step-by-step")
    lines.append("")
    lines.append("1. Sign in to the AWS Console at <https://console.aws.amazon.com>.")
    lines.append("2. In the top search bar, type **S3** and click the S3 service.")
    lines.append("3. From the bucket list, click into **`help-media.stemcounts.com`**.")
    lines.append("4. Click the orange **Upload** button (top-right).")
    lines.append("5. Drag your captured files into the drop zone (or click **Add files** and pick them).")
    lines.append("6. Leave all the default options as they are. Don't create folders.")
    lines.append("7. Click **Upload** at the bottom.")
    lines.append("")
    lines.append("Once a batch is uploaded, the images will appear on the live help site after the next docs rebuild (usually within a few hours, or sooner if you ping the dev team to trigger one).")
    lines.append("")
    lines.append("### Filename rules")
    lines.append("")
    lines.append("- Use the **exact filename** shown in each section below. Copy the code block — don't retype it.")
    lines.append("- Extensions matter: `.png` for screenshots, `.mp4` for short videos.")
    lines.append("- No spaces, no capitals, no folder paths.")
    lines.append("")
    lines.append("### Capture guidelines")
    lines.append("")
    lines.append("- **Screenshots**: capture at 2× (Retina) for crispness; aim for around 2400px wide max.")
    lines.append("- **Videos**: MP4, H.264, max 1080p, ideally under 20 MB and under 30 seconds.")
    lines.append("- **Redact**: blur or replace any real florist names, customer names, real prices, or addresses before saving.")
    lines.append("")
    lines.append("If you don't have AWS access, send the captured files to whoever does — the upload step is just drag-and-drop and takes seconds.")
    lines.append("")

    # ── Per-article sections ──────────────────────────────────────────
    lines.append("## What to capture")
    lines.append("")
    lines.append(
        "Each section below is one article on the help site. The article link opens "
        "the live page so you can see the context the image / video sits in. The code "
        "block is the **exact filename** to save the captured file as — click the copy "
        "icon in the top-right of the block."
    )
    lines.append("")

    # Order articles by section, then alphabetically within each section.
    def article_sort_key(url: str) -> tuple[int, str]:
        sec = section_of(url)
        try:
            order = SECTION_ORDER.index(sec)
        except ValueError:
            order = len(SECTION_ORDER)
        return (order, url)

    for url in sorted(by_article.keys(), key=article_sort_key):
        refs = by_article[url]
        # All refs in this article share the same title; pick from first.
        title = refs[0].article_title
        lines.append(f"### [{title}]({url})")
        lines.append("")

        # Group by slug so duplicates inside the same article aren't listed twice.
        seen_slugs: dict[str, Reference] = {}
        for ref in refs:
            seen_slugs.setdefault(ref.slug, ref)

        for slug, ref in seen_slugs.items():
            ext = "mp4" if ref.kind == "video" else "png"
            filename = f"{slug}.{ext}"
            kind_tag = "**🎥 video**" if ref.kind == "video" else "image"

            lines.append(f"- [ ] {kind_tag}")
            lines.append("")
            lines.append("  ```")
            lines.append(f"  {filename}")
            lines.append("  ```")
            lines.append("")
            if ref.caption:
                lines.append(f"  *Shows:* {ref.caption}")
                lines.append("")

        lines.append("")  # spacing between articles

    # ── Quick alphabetical lookup ─────────────────────────────────────
    lines.append("---")
    lines.append("")
    lines.append("## Quick alphabetical lookup")
    lines.append("")
    lines.append("If you need to find a specific filename fast:")
    lines.append("")
    for slug in sorted(unique_slugs):
        # Find the kind from any reference for this slug.
        ref_for_slug = next(r for r in references if r.slug == slug)
        ext = "mp4" if ref_for_slug.kind == "video" else "png"
        lines.append(f"- `{slug}.{ext}` → [{ref_for_slug.article_title}]({ref_for_slug.article_url})")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"Wrote {OUT.relative_to(REPO_ROOT)} — "
        f"{len(unique_slugs)} unique files "
        f"({image_count} images, {len(video_slugs)} videos) "
        f"across {len(by_article)} articles."
    )


if __name__ == "__main__":
    main()
