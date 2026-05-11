/**
 * Help-media URL helper.
 *
 * Pattern: each `<HelpMedia id="slug" />` resolves directly to
 *
 *   `${BASE_URL}/${slug}.${ext}`
 *
 * where `ext` is `png` for images and `mp4` for videos. No manifest,
 * no DB, no Lambda — Kate (or anyone) drops a file into the S3 bucket
 * with the matching filename and it shows up on the next build (and
 * after CDN cache TTL).
 *
 * When the in-app admin UI gets built later, this is the file to swap
 * out: replace the URL-convention call with a lookup against whatever
 * DDB / manifest the admin UI produces. See planease-help's
 * src/lib/manifest.ts for the full denormalized-manifest pattern.
 */

const DEFAULT_BASE_URL = "https://help-media.stemcounts.com";

/**
 * Base URL for help-media. Override at build time via
 * PUBLIC_HELP_MEDIA_BASE_URL (set in .env locally or in Amplify env
 * vars per branch — useful for a staging bucket).
 *
 * Trailing slashes are stripped so callers can append `/{slug}.{ext}`
 * unconditionally.
 */
export const HELP_MEDIA_BASE_URL = (
  import.meta.env.PUBLIC_HELP_MEDIA_BASE_URL ?? DEFAULT_BASE_URL
).replace(/\/$/, "");

export type HelpMediaKind = "image" | "video";

/** Default file extension per media kind. Standardised so Kate doesn't
 *  have to think about format — convert source files to png / mp4 before
 *  upload. Override via the `ext` prop on `<HelpMedia>` if needed. */
const DEFAULT_EXT: Record<HelpMediaKind, string> = {
  image: "png",
  video: "mp4",
};

export function helpMediaUrl(
  slug: string,
  kind: HelpMediaKind = "image",
  ext?: string,
): string {
  const finalExt = ext ?? DEFAULT_EXT[kind];
  return `${HELP_MEDIA_BASE_URL}/${slug}.${finalExt}`;
}

/**
 * Best-effort humanised alt text for a slug, used as a fallback when
 * the article author hasn't provided one. `florist-landing-overview`
 * becomes "Florist landing overview". Articles should still pass
 * explicit `alt=` for anything load-bearing — accessibility matters
 * more than a clever default.
 */
export function humanizeSlug(slug: string): string {
  const spaced = slug.replace(/[-_]+/g, " ").trim();
  if (!spaced) return "";
  return spaced.charAt(0).toUpperCase() + spaced.slice(1);
}
