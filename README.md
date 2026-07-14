# ML Paper Icons

> A curated set of **512 free, commercial-safe vector icons** for AI / ML / multimodal / LLM / NLP / Agent research papers — with a searchable gallery, one-click recolor, and copy-as-SVG/PNG.

![icons](https://img.shields.io/badge/icons-512-2563eb)
![license](https://img.shields.io/badge/license-MIT%2FISC-green)
![attribution](https://img.shields.io/badge/attribution-not%20required-brightgreen)

[中文说明 (Chinese README)](README-zh.md) · [Live gallery](https://Mizar77.github.io/ml-paper-icons/)

No more hunting on Flaticon and dodging attribution requirements. Every icon
here comes from a permissively licensed open-source library (Lucide / Tabler /
Phosphor / Lobe Icons), is a clean transparent SVG, and can be dropped straight
into draw.io, Figma, PowerPoint, or LaTeX.

## Why this exists

Making a good method figure needs the right icons, but:
- **Flaticon's free tier requires attribution** in your paper and limits SVG access.
- Icons are scattered across many libraries with different licenses.
- Paper figures need **mono icons you recolor by semantics** (input=blue, encoder=green, novel=red…), not flashy multicolor clipart.

This repo solves all three: pre-curated by ML paper scenario, license-clean, and recolorable.

## What's inside

| Category | Count | Library | License | Recolorable |
|----------|-------|---------|---------|:-----------:|
| `icons/lucide/`   | 177 | [Lucide](https://lucide.dev)            | ISC | ✅ |
| `icons/tabler/`   | 131 | [Tabler](https://tabler.io/icons)       | MIT | ✅ |
| `icons/phosphor/` | 114 | [Phosphor](https://phosphoricons.com)   | MIT | ✅ |
| `icons/duotone/`  |  51 | Phosphor (duotone)                      | MIT | ✅ |
| `icons/brand/`    |  39 | [Lobe Icons](https://github.com/lobehub/lobe-icons) — OpenAI/Claude/Gemini/HF/PyTorch… | MIT | ❌ (full color) |

Organized by 12 paper-oriented themes: Vision, Audio, NLP/Text, LLM/Generation,
Model/Architecture, Data/Storage, Training/Optim, Eval/Charts, Math/Symbols,
Agent/Tools, Results, Flow.

> **Can't find the icon you need?** Try [Flaticon](https://www.flaticon.com/) — a
> much larger library. Note: its free tier **requires attribution** in your paper
> (or a paid plan to skip it), and free SVGs are often locked to PNG. The icons in
> this repo are attribution-free by contrast.

## Live gallery

Open **[the gallery](https://Mizar77.github.io/ml-paper-icons/)** (GitHub Pages),
or open `docs/index.html` locally. Features:

- 🔎 Search by name, filter by library
- 🎨 **Palette** — recolor all mono icons at once; the copied SVG/PNG keeps the color
- 📋 **Click** a card to copy SVG code (paste into draw.io/Figma → editable vector)
- 🖼️ Hover → **PNG** (copy as image) or **↓** (download .svg)

## Usage

### draw.io / Figma
Click an icon in the gallery to copy its SVG, then paste directly onto the canvas — it becomes an editable vector object.

### LaTeX
```bash
# Convert SVG to PDF (keeps it vector)
inkscape --export-filename=brain.pdf icons/lucide/brain.svg
```
```latex
\includegraphics[height=1em]{brain}
% or with the svg package:
\usepackage{svg}
\includesvg[height=1em]{icons/lucide/brain}   % needs --shell-escape + inkscape
```

### Recolor manually
Mono icons use `stroke="currentColor"`. Change `stroke`/`color` to any hex value:
```bash
sed 's/currentColor/#E74C3C/g' icons/lucide/brain.svg > brain-red.svg
```

## Reproduce / update the set

Everything is scripted and reproducible from `scripts/manifest.json`:

```bash
python3 scripts/fetch_icons.py          # re-download all icons from upstream CDNs
python3 scripts/fetch_icons.py --check  # verify local files match the manifest
python3 scripts/build_gallery.py        # rebuild docs/index.html
```

To add icons: edit `scripts/manifest.json`, run `fetch_icons.py`, then `build_gallery.py`.

## License

- Original work in this repo (scripts, gallery, curation, docs): **MIT** — see [LICENSE](LICENSE).
- The icon SVGs keep their upstream licenses (all ISC/MIT, commercial-safe, no attribution required) — see [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
- **Brand logos** are trademarks of their owners; the MIT license covers the SVG code, not trademark rights. See the note in THIRD_PARTY_LICENSES.md.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs that add paper-relevant icons or new
permissively-licensed sources are welcome.
