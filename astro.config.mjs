// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import sitemap from "@astrojs/sitemap";

// StemCounts help / docs site.
// Single Starlight project — content is grouped into product-area
// sections via the sidebar. Each section is a folder under
// src/content/docs/. Adding a new article = add a new .mdx file in
// the right folder; Starlight picks it up automatically.
export default defineConfig({
  // Canonical site URL — drives OG tags, sitemap entries, and the
  // <link rel="canonical"> on every page. Update if the domain ever
  // changes; the value here must match the live host exactly.
  site: "https://help.stemcounts.com",
  integrations: [
    // Explicit sitemap integration. Starlight emits one by default,
    // but we want explicit control so future tweaks (filtering,
    // priorities, lastmod) have a clear hook. Output is at
    // /sitemap-index.xml; robots.txt points at it.
    sitemap(),
    starlight({
      title: "StemCounts Help",
      description:
        "Guides, walkthroughs, and reference for StemCounts — flower ordering for florists and wholesalers.",
      // Single-file logo (coral + teal flower mark). The same SVG
      // works on light and dark backgrounds because both fills are
      // mid-saturation. Swap to a dark-specific variant in
      // src/assets/ if contrast ever feels off.
      logo: {
        src: "./src/assets/stemcounts-logo.svg",
        replacesTitle: false,
      },
      // Custom CSS owns design-system mapping (Inter font, forest
      // green accent, coral CTA, neutral slate grays). See
      // src/styles/custom.css — comment block at the top documents
      // the source of each token.
      customCss: ["./src/styles/custom.css"],
      // No "Edit on GitHub" link. Content authoring happens elsewhere
      // (TBD pipeline); external PR-driven edits aren't a workflow
      // we're set up for yet.
      social: [],
      // Component overrides:
      //   - SocialIcons → "Sign in" CTA pointing at the main app
      //     (HeaderActions.astro)
      //   - ThemeSelect → custom sun/moon icon toggle (replaces the
      //     Light/Dark/Auto dropdown that Starlight ships with)
      components: {
        SocialIcons: "./src/components/HeaderActions.astro",
        ThemeSelect: "./src/components/CustomThemeToggle.astro",
      },
      sidebar: [
        { label: "Getting started", autogenerate: { directory: "getting-started" } },
        { label: "Ordering", autogenerate: { directory: "ordering" } },
        { label: "Inventory", autogenerate: { directory: "inventory" } },
        { label: "Suppliers (wholesalers)", autogenerate: { directory: "suppliers" } },
        { label: "Customers (florists)", autogenerate: { directory: "customers" } },
        { label: "Account & billing", autogenerate: { directory: "billing" } },
        { label: "Release notes", autogenerate: { directory: "changelog" } },
      ],
      // Quick search built in via Pagefind — no extra setup needed.
    }),
  ],
});
