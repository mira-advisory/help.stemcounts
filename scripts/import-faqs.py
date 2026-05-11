#!/usr/bin/env python3
"""
One-shot importer for faqdata.json → src/content/docs/faqs/*.mdx.

Reads the existing FAQ data from the main StemCounts app
(`builder-sc-frontend/src/pages/florist/faqdata.json`) and emits one
MDX file per `categorypage`. Each Q becomes an H2; each A is the
paragraph below; Scribehow walkthrough URLs are embedded as iframes
where present.

Run from the repo root:

    python scripts/import-faqs.py

Idempotent: it overwrites every output file every run, so re-running
after a faqdata.json update refreshes the docs side without manual
merging.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = (
    REPO_ROOT.parent
    / "builder-sc-frontend"
    / "src"
    / "pages"
    / "florist"
    / "faqdata.json"
)
OUT_DIR = REPO_ROOT / "src" / "content" / "docs" / "faqs"

# Category metadata: slug, title, description, sidebar order.
CATEGORIES = {
    "Florists": {
        "slug": "florists",
        "title": "Florist FAQs",
        "description": "Common questions about orders, events, arrangements, the catalog, and the Spares Bucket.",
        "order": 1,
    },
    "Wholesalers": {
        "slug": "wholesalers",
        "title": "Wholesaler FAQs",
        "description": "Common questions about the Order Board, supplier assignment, and fulfilment.",
        "order": 2,
    },
    "Finances": {
        "slug": "finances",
        "title": "Finances FAQs",
        "description": "Pricing, budgets, GST, invoicing, and subscription billing.",
        "order": 3,
    },
    "Setup": {
        "slug": "setup",
        "title": "Setup FAQs",
        "description": "First-time configuration: account, organisation, and retail markup.",
        "order": 4,
    },
    "Delivery": {
        "slug": "delivery",
        "title": "Delivery FAQs",
        "description": "Delivery windows, cut-offs, and what happens when something runs late.",
        "order": 5,
    },
}

SCRIBEHOW_RE = re.compile(r"https://scribehow\.com/(?:embed|viewer)/[A-Za-z0-9_\-]+")


def split_urls(field: str) -> list[str]:
    """Pull out clean Scribehow URLs from a freeform `guideurl` field.

    The source data sometimes concatenates multiple URLs with commas, or
    runs them together with no separator. The regex captures each one
    individually so badly-formatted fields still yield usable links.
    """
    if not field:
        return []
    return list(dict.fromkeys(SCRIBEHOW_RE.findall(field)))  # dedupe, preserve order


def embed_url(url: str) -> str:
    """Convert a Scribehow viewer URL into the embed form."""
    return url.replace("/viewer/", "/embed/", 1)


def render_entry(entry: dict) -> str:
    """Render one FAQ Q&A as MDX."""
    q = entry.get("question", "").strip()
    a = entry.get("answer", "").strip()
    element = entry.get("element", "").strip()
    page_route = entry.get("pageroute", "").strip()
    guide_title = entry.get("guidetitle", "").strip()
    urls = split_urls(entry.get("guideurl", ""))

    parts: list[str] = []
    parts.append(f"## {q}")
    parts.append("")
    if a:
        parts.append(a)
        parts.append("")

    # Contextual hints (where in the app, which UI element)
    hints: list[str] = []
    if page_route and page_route.startswith("/"):
        hints.append(f"**Where:** `{page_route}` in the app")
    if element:
        hints.append(f"**UI element:** {element}")
    if hints:
        parts.append(" · ".join(hints))
        parts.append("")

    # Walkthrough video(s)
    if urls:
        if guide_title:
            parts.append(f"**{guide_title}**")
            parts.append("")
        for url in urls:
            embed = embed_url(url)
            parts.append(
                f'<iframe src="{embed}" width="100%" height="640" '
                f'allow="fullscreen" frameborder="0" '
                f'title="Scribehow walkthrough"></iframe>'
            )
            parts.append("")

    return "\n".join(parts)


def render_category(name: str, entries: list[dict]) -> str:
    """Render one category's MDX file."""
    meta = CATEGORIES[name]
    # Quote the description in case it contains YAML-significant chars
    # like `:` — js-yaml is strict about unquoted colons in scalars.
    desc_escaped = meta["description"].replace('"', '\\"')
    frontmatter = (
        "---\n"
        f"title: {meta['title']}\n"
        f'description: "{desc_escaped}"\n'
        f"sidebar:\n  order: {meta['order']}\n"
        "---\n\n"
    )

    intro = (
        f"These are the same {name.lower()}-focused FAQ entries shown inside "
        "the StemCounts app under **FAQ** in the user menu. Each entry "
        "links to a step-by-step Scribehow walkthrough where one exists.\n\n"
    )

    body = "\n".join(render_entry(e) for e in entries)
    return frontmatter + intro + body + "\n"


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit(f"Expected list at {SOURCE}, got {type(data).__name__}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # The source data uses `categorypage` for both topic categories
    # (Florists, Wholesalers, etc.) AND page-level groupings (Orders,
    # Settings, Receive & Accept, ...). Map the page-level ones into
    # the right topic bucket so nothing is dropped.
    page_to_topic = {
        # Florist-side pages
        "Orders": "Florists",
        "Order Details": "Florists",
        "Order Part Details": "Florists",
        "Dashboard": "Florists",
        "Flower Picker": "Florists",
        # Wholesaler-side pages
        "Receive & Accept": "Wholesalers",
        "Assign & Send": "Wholesalers",
        "Confirmed & Ready": "Wholesalers",
        "Assigned Orders": "Wholesalers",
        # Setup-shaped pages
        "Register": "Setup",
        "Settings": "Setup",
        "FAQs": "Setup",
    }

    # Bucket entries by category, preserving source order.
    buckets: dict[str, list[dict]] = {k: [] for k in CATEGORIES}
    skipped: list[str] = []
    for entry in data:
        cat = (entry.get("categorypage") or "").strip()
        cat = page_to_topic.get(cat, cat)
        if cat in buckets:
            buckets[cat].append(entry)
        else:
            skipped.append(cat or "(empty)")

    total = 0
    for name, entries in buckets.items():
        if not entries:
            # Still write a placeholder so the section renders something.
            entries = []
        out = OUT_DIR / f"{CATEGORIES[name]['slug']}.mdx"
        out.write_text(render_category(name, entries), encoding="utf-8")
        print(f"  wrote {out.name} ({len(entries)} entries)")
        total += len(entries)

    if skipped:
        print(f"  skipped {len(skipped)} entries with unknown category: {set(skipped)}")
    print(f"Done. {total} entries written across {len(CATEGORIES)} category files.")


if __name__ == "__main__":
    main()
