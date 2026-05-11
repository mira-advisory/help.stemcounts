/**
 * Build-time fetcher for the help-media manifest.
 *
 * Pattern mirrors planease-help: each `<HelpMedia id="slug" />` instance
 * resolves its id against a flat manifest.json published to S3 by an
 * upstream Lambda. The manifest is fetched once per Astro build and
 * cached at module scope.
 *
 * NOTE — pipeline status:
 *   At the time this repo was bootstrapped, the StemCounts help-media
 *   pipeline (S3 bucket + manifest-writer Lambda) does NOT exist yet.
 *   The default URL below is a placeholder. Until the pipeline is
 *   stood up, the fetch will fail and <HelpMedia> renders a visible
 *   missing-media placeholder instead of failing the build.
 *
 * Override the URL at build time via the PUBLIC_HELP_MEDIA_MANIFEST_URL
 * env var (set in .env locally, or in Amplify env vars per branch).
 */

const DEFAULT_MANIFEST_URL =
  "https://help-media.stemcounts.com/manifest.json";

const MANIFEST_URL =
  import.meta.env.PUBLIC_HELP_MEDIA_MANIFEST_URL ?? DEFAULT_MANIFEST_URL;

export interface HelpMediaItem {
  slug: string;
  kind: "screenshot" | "video";
  page_key: string;
  url: string;
  content_type: string;
  alt: string | null;
  caption: string | null;
  tags: string[] | null;
  size_bytes: number | null;
}

export interface HelpMediaManifest {
  version: number;
  generated_at: string;
  count: number;
  items: HelpMediaItem[];
}

let cached: Map<string, HelpMediaItem> | null = null;
let cachedManifest: HelpMediaManifest | null = null;

async function loadManifest(): Promise<HelpMediaManifest> {
  if (cachedManifest) return cachedManifest;

  try {
    const res = await fetch(MANIFEST_URL, {
      headers: { "cache-control": "no-cache" },
    });
    if (!res.ok) {
      // eslint-disable-next-line no-console
      console.warn(
        `[help-media] manifest fetch failed (${res.status}); placeholders will render. URL=${MANIFEST_URL}`,
      );
      cachedManifest = { version: 0, generated_at: "", count: 0, items: [] };
      return cachedManifest;
    }
    const json = (await res.json()) as HelpMediaManifest;
    if (json.version !== 1) {
      // eslint-disable-next-line no-console
      console.warn(
        `[help-media] manifest version drift (got ${json.version}, expected 1)`,
      );
    }
    cachedManifest = json;
    return json;
  } catch (err) {
    // eslint-disable-next-line no-console
    console.warn(
      `[help-media] manifest fetch threw; placeholders will render.`,
      err,
    );
    cachedManifest = { version: 0, generated_at: "", count: 0, items: [] };
    return cachedManifest;
  }
}

export async function getHelpMedia(slug: string): Promise<HelpMediaItem | null> {
  if (!cached) {
    const m = await loadManifest();
    cached = new Map(m.items.map((it) => [it.slug, it]));
  }
  return cached.get(slug) ?? null;
}

export async function getAllHelpMedia(): Promise<HelpMediaItem[]> {
  const m = await loadManifest();
  return m.items;
}
