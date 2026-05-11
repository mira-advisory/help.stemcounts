#!/usr/bin/env python3
"""
Generate a markdown checklist of every <HelpMedia> slug referenced in
articles, with article context and caption where present, so a
non-technical team member can work through it and upload screenshots
into the S3 bucket one by one.

Output: docs/HELP_MEDIA_CHECKLIST.md (overwritten on each run).

Run from repo root:

    python scripts/list-help-media.py
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "src" / "content" / "docs"
OUT = REPO_ROOT / "docs" / "HELP_MEDIA_CHECKLIST.md"

# Match <HelpMedia ...id="slug"... />, capturing the slug and the
# remainder of the tag for attribute parsing.
TAG_RE = re.compile(
    r"<HelpMedia\b([^/>]*?)\bid\s*=\s*\"([^\"]+)\"([^/>]*)/?>",
    re.MULTILINE,
)
ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')


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


def main() -> None:
    # slug -> list of (article_path, article_title, kind, caption)
    refs: dict[str, list[tuple[str, str, str, str | None]]] = defaultdict(list)

    for mdx in sorted(DOCS.rglob("*.mdx")):
        text = mdx.read_text(encoding="utf-8")
        title = article_title(mdx)
        rel_url = "/" + mdx.relative_to(DOCS).as_posix().replace(".mdx", "").replace("/index", "/") + "/"
        rel_url = rel_url.replace("//", "/").rstrip("/") + "/"

        for m in TAG_RE.finditer(text):
            pre, slug, post = m.group(1), m.group(2), m.group(3)
            attrs = parse_attrs(pre, post)
            kind = attrs.get("kind", "image")
            caption = attrs.get("caption")
            refs[slug].append((rel_url, title, kind, caption))

    # Group by kind for the summary header
    by_kind: dict[str, int] = defaultdict(int)
    for slug, uses in refs.items():
        # If any usage marks it as video, treat the whole slug as video
        kinds = {u[2] for u in uses}
        primary_kind = "video" if "video" in kinds else "image"
        by_kind[primary_kind] += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# Help-media upload checklist")
    lines.append("")
    lines.append(
        "Every `<HelpMedia id=\"slug\" />` reference in the articles, listed "
        "here so whoever is capturing screenshots / video walkthroughs can "
        "work through it methodically."
    )
    lines.append("")
    lines.append("## How to upload")
    lines.append("")
    lines.append("1. Capture the screenshot or short video for the slug below.")
    lines.append("2. Save the file with the **exact** filename shown — kebab-case slug + `.png` (images) or `.mp4` (videos).")
    lines.append("3. Upload to the S3 bucket: **`help-media.stemcounts.com`** (flat at the root, no folders).")
    lines.append("4. After a batch of uploads, ping the dev team to trigger a docs site rebuild — or wait for the next deploy.")
    lines.append("")
    lines.append("## Conventions")
    lines.append("")
    lines.append("- **Resolution**: capture at 2× (Retina) so the docs look crisp; aim for a max width of 2400px.")
    lines.append("- **Image format**: PNG. Convert JPGs to PNG before upload.")
    lines.append("- **Video format**: MP4, H.264, max 1080p, keep under 20 MB where you can.")
    lines.append("- **Don't include sensitive data**: redact real florist / customer names, real prices, real addresses.")
    lines.append("")
    lines.append(f"## Slugs to upload — {len(refs)} total ({by_kind.get('image', 0)} images, {by_kind.get('video', 0)} videos)")
    lines.append("")

    for slug in sorted(refs):
        uses = refs[slug]
        kinds = {u[2] for u in uses}
        primary_kind = "video" if "video" in kinds else "image"
        ext = "mp4" if primary_kind == "video" else "png"
        lines.append(f"### `{slug}.{ext}`")
        lines.append("")
        for rel_url, title, _, caption in uses:
            entry = f"- **[{title}]({rel_url})**"
            if caption:
                entry += f" — caption: *{caption}*"
            lines.append(entry)
        lines.append("")
        lines.append("- [ ] Captured")
        lines.append("- [ ] Uploaded to S3")
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(REPO_ROOT)} ({len(refs)} unique slugs)")


if __name__ == "__main__":
    main()
