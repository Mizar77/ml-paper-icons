# Contributing

Thanks for helping improve ML Paper Icons!

## Adding icons

**Do not commit hand-downloaded SVGs directly.** Everything is driven by the
manifest so the set stays reproducible and license-clean.

1. Find the icon in a permissively-licensed library (ISC / MIT / Apache-2.0 /
   CC0). Good sources: Lucide, Tabler, Phosphor, Lobe Icons, Remix Icon,
   Heroicons, Iconoir, Bootstrap Icons, Simple Icons.
2. Add its name to `scripts/manifest.json` under the right group.
3. Regenerate:
   ```bash
   python3 scripts/fetch_icons.py
   python3 scripts/build_gallery.py
   ```
4. Commit the new SVGs under `icons/`, the updated `manifest.json`, and
   `docs/index.html`.

## Adding a new source library

If you want to pull from a library not yet supported:
1. Add a new group to `manifest.json`.
2. Extend `build_url_map()` in `scripts/fetch_icons.py` with the CDN URL pattern.
3. Add the library to `THIRD_PARTY_LICENSES.md` with its license and source.
4. **Verify the license permits redistribution and commercial use.** Reject
   anything requiring attribution-in-product or with non-commercial clauses.

## Guidelines

- Prefer **mono, stroke-based** icons that recolor cleanly.
- Keep names descriptive and lowercase-with-hyphens.
- Don't add decorative/off-topic icons — this set is scoped to ML/AI papers.
- For brand logos, respect trademark guidelines (see THIRD_PARTY_LICENSES.md).

## Reporting issues

Open an issue for: broken CDN URLs, wrong categorization, missing common icons,
or license concerns.
