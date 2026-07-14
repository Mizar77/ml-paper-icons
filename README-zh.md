# ML Paper Icons · 论文方法图图标库

> 为 AI / 机器学习 / 多模态 / 大模型（LLM） / NLP / 智能体（Agent）论文准备的 **512 个免费矢量图标**——自带可搜索画廊、一键换色、复制 SVG/PNG。

![icons](https://img.shields.io/badge/icons-512-2563eb)
![license](https://img.shields.io/badge/license-MIT%2FISC-green)
![attribution](https://img.shields.io/badge/署名-无需-brightgreen)

[English README](README.md) · [在线画廊](https://Mizar77.github.io/ml-paper-icons/)

再也不用在 Flaticon 上一个个找、还要担心署名问题。这里每个图标都来自宽松许可的开源图标库（Lucide / Tabler / Phosphor / Lobe Icons），都是干净的透明 SVG，可以直接拖进 draw.io、Figma、PowerPoint 或 LaTeX。

## 为什么做这个

画一张好的方法图需要合适的图标，但现实中：
- **Flaticon 免费档要求在论文里署名**，而且免费 SVG 受限、批量下载违反其服务条款。
- 图标散落在很多库里，许可证五花八门，逐个确认很麻烦。
- 论文图需要的是**单色、按语义上色**的图标（输入=蓝、编码器=绿、创新点=红……），而不是花花绿绿的插画。

这个仓库一次解决三个问题：按论文场景预筛选、许可证干净、可随意换色。

## 有什么

| 类别 | 数量 | 来源库 | 许可 | 可换色 |
|------|------|--------|------|:------:|
| `icons/lucide/`   | 177 | [Lucide](https://lucide.dev)            | ISC | ✅ |
| `icons/tabler/`   | 131 | [Tabler](https://tabler.io/icons)       | MIT | ✅ |
| `icons/phosphor/` | 114 | [Phosphor](https://phosphoricons.com)   | MIT | ✅ |
| `icons/duotone/`  |  51 | Phosphor（双色）                        | MIT | ✅ |
| `icons/brand/`    |  39 | [Lobe Icons](https://github.com/lobehub/lobe-icons)——OpenAI/Claude/Gemini/HF/PyTorch 等 | MIT | ❌（固有彩色）|

按 12 个论文场景主题归类：视觉图像、语音音频、NLP文本、大模型生成、模型架构、数据存储、训练优化、评估图表、数学符号、智能体工具、结果判定、流程其他。

## 在线画廊

打开 **[在线画廊](https://Mizar77.github.io/ml-paper-icons/)**（GitHub Pages），或在本地打开 `docs/index.html`。功能：

- 🔎 按名称搜索、按库筛选
- 🎨 **调色板**——一键给所有单色图标换色，复制出来的 SVG/PNG 会带上该颜色
- 📋 **单击**卡片复制 SVG 代码（粘进 draw.io/Figma 即为可编辑矢量）
- 🖼️ 悬停 → **PNG**（复制成图片）或 **↓**（下载 .svg）

## 怎么用

### draw.io / Figma
在画廊里单击图标复制其 SVG，直接在画布上粘贴，即变成可编辑的矢量对象。

### LaTeX
```bash
# 先转 PDF（保留矢量）
inkscape --export-filename=brain.pdf icons/lucide/brain.svg
```
```latex
\includegraphics[height=1em]{brain}
% 或用 svg 宏包：
\usepackage{svg}
\includesvg[height=1em]{icons/lucide/brain}   % 需 --shell-escape + inkscape
```

### 手动换色
单色图标用 `stroke="currentColor"`，把 `stroke`/`color` 改成任意十六进制色值即可：
```bash
sed 's/currentColor/#E74C3C/g' icons/lucide/brain.svg > brain-red.svg
```

## 复现 / 更新图标集

所有图标都由 `scripts/manifest.json` 驱动，可完全复现：

```bash
python3 scripts/fetch_icons.py          # 从上游 CDN 重新下载全部图标
python3 scripts/fetch_icons.py --check  # 校验本地文件与清单是否一致
python3 scripts/build_gallery.py        # 重新生成 docs/index.html
```

想加图标：编辑 `scripts/manifest.json`，跑 `fetch_icons.py`，再跑 `build_gallery.py`。

## 许可

- 本仓库的原创部分（脚本、画廊、整理、文档）：**MIT** —— 见 [LICENSE](LICENSE)。
- 图标 SVG 保留各自上游许可（均为 ISC/MIT，可商用、免署名）—— 见 [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)。
- **品牌 Logo** 是各公司的商标；MIT 许可只覆盖 SVG 代码，不含商标权。在论文里用来表示"我们用了某模型/框架"通常属于合理的指代性使用，但不要暗示获得对方背书。详见 THIRD_PARTY_LICENSES.md。

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。欢迎提交与论文相关的图标或新的宽松许可来源。
