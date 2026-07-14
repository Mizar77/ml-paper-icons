#!/usr/bin/env python3
"""Build the searchable icon gallery (docs/index.html) from the icons/ directory.

Run after fetch_icons.py:
    python3 scripts/build_gallery.py

Output: docs/index.html  (served by GitHub Pages)
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(ROOT, "icons")
OUT = os.path.join(ROOT, "docs", "index.html")


def load_svg(path):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    if "-->" in s and s.strip().startswith("<!--"):
        s = s.split("-->", 1)[1]
    return s.strip()


def collect(folder):
    d = os.path.join(ICONS, folder)
    out = {}
    if not os.path.isdir(d):
        return out
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".svg"):
            out[fn[:-4]] = load_svg(os.path.join(d, fn))
    return out


mono = {
    "lucide":   {"data": collect("lucide"),   "label": "Lucide"},
    "tabler":   {"data": collect("tabler"),   "label": "Tabler"},
    "phosphor": {"data": collect("phosphor"), "label": "Phosphor"},
}
color = {
    "brand":   {"data": collect("brand"),   "label": "Brand logo"},
    "duotone": {"data": collect("duotone"), "label": "Duotone"},
}
alllabels = {**{k: v["label"] for k, v in mono.items()},
             **{k: v["label"] for k, v in color.items()}}

themes = [
 ("Vision & Image / 视觉图像", ["image","photo","camera","film","video","frame","crop","aperture","perspective","dimension","3d","cube","bounding","photo-scan","scan-position","color-swatch","palette","swatch","eyedropper","contrast","focus","smile","smiley","detective","binocular","face","selection"]),
 ("Audio & Speech / 语音音频", ["audio","music","wave","waveform","volume","speaker","headphone","mic","microphone","radio","vocal","sine"]),
 ("NLP & Text / 文本", ["text","language","translate","abc","alphabet","letter","case","word","pilcrow","spell","vocab","tag","tags","bookmark","quote","quotes","article","caption","aa","-t","paragraph","highlighter","pen-nib","note","book"]),
 ("LLM & Generation / 大模型生成", ["brain","cpu","circuit","chip","gpt","openai","google","prompt","sparkle","wand","lightbulb","bulb","filament","terminal","command","token","keyframe"]),
 ("Model & Architecture / 模型架构", ["network","layer","stack","node","tree","graph","hierarchy","topology","sitemap","block","box-model","component","puzzle","transform","matrix","vector","spiral","waypoint","spline","circuit-board","memory-stick","atom","affiliate","cable","webhook"]),
 ("Data & Storage / 数据存储", ["database","server","cloud","hard-drive","grid","table","binary","hash","numbers","decimal","fingerprint","clipboard-data","file-analytics","file-json","dna"]),
 ("Training & Optim. / 训练优化", ["setting","slider","adjust","cog","gear","gauge","activity","zap","bolt","lightning","flame","temperature","thermometer","refresh","rotate","repeat","recycle","arrows-clock","git","fork","merge","split","regression","diff","fold","unfold","combine","group","transform-point"]),
 ("Eval & Charts / 评估图表", ["target","crosshair","scan","eye","chart","trending","histogram","ppf","analytics","report","math-avg","regress","dots"]),
 ("Math & Symbols / 数学符号", ["math","sigma","function","integral","sum","square-root","radical","divide","asterisk","percent","plus","minus","equal","infinity","pi","variable","operation","dice"]),
 ("Agent & Tools / 智能体工具", ["robot","bot","tool","tools","wrench","api","plug","route","map","strategy","message","chat","chats","send","world","flow","signpost","user","users","people","share","code","brace","bracket","regex","xml","wifi","funnel","shuffle","search","magnify","zoom"]),
 ("Results / 结果判定", ["check","circle-check","circle-x","-x","thumbs","award","trophy","medal","flag","star","flask","test-tube","microscope"]),
 ("Flow & Misc / 流程其他", ["arrow","play","lock","unlock","key","shield","clock","timer","calendar","history","countdown","download","upload","save","list","anchor"]),
]


def theme_of(name):
    low = name.lower()
    for tname, kws in themes:
        for kw in kws:
            if kw in low:
                return tname
    return "Flow & Misc / 流程其他"


def cell(lk, name, svg, colorable):
    cls = "cell colorable" if colorable else "cell fixedcolor"
    return (f'<div class="{cls}" data-name="{name}" data-lib="{lk}" onclick="copySVG(this)">'
            f'<div class="acts"><button class="act" title="Copy PNG" onclick="event.stopPropagation();copyPNG(this)">PNG</button>'
            f'<button class="act" title="Download SVG" onclick="event.stopPropagation();dl(this)">&#8595;</button></div>'
            f'<div class="ic">{svg}</div><div class="nm">{name}</div><div class="tag">{alllabels[lk]}</div></div>')


sections = []
brand_items = sorted(color["brand"]["data"].items())
if brand_items:
    cells = [cell("brand", n, s, False) for n, s in brand_items]
    sections.append(f'<section class="cat"><h2>Brand / LLM vendor logos · 厂商彩色 Logo <span class="cnt">{len(cells)}</span> <span class="badge">full color · lobe-icons MIT</span></h2><div class="grid">{"".join(cells)}</div></section>')

duo_items = sorted(color["duotone"]["data"].items())
if duo_items:
    cells = [cell("duotone", n, s, True) for n, s in duo_items]
    sections.append(f'<section class="cat"><h2>Duotone · 双色（可上色）<span class="cnt">{len(cells)}</span> <span class="badge">Phosphor MIT</span></h2><div class="grid">{"".join(cells)}</div></section>')

buckets = {t[0]: [] for t in themes}
for lk, meta in mono.items():
    for name, svg in meta["data"].items():
        buckets[theme_of(name)].append((lk, name, svg))
for tname, _ in themes:
    items = sorted(buckets[tname], key=lambda x: (x[1], x[0]))
    if not items:
        continue
    cells = [cell(lk, n, s, True) for lk, n, s in items]
    sections.append(f'<section class="cat"><h2>{tname} <span class="cnt">{len(cells)}</span></h2><div class="grid">{"".join(cells)}</div></section>')

total = sum(len(m["data"]) for m in mono.values()) + sum(len(c["data"]) for c in color.values())
ml, mt, mp = (len(mono[k]["data"]) for k in ("lucide", "tabler", "phosphor"))
cb, cd = len(color["brand"]["data"]), len(color["duotone"]["data"])

TEMPLATE = r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ML Paper Icons — free icons for AI / ML / LLM / NLP / Agent papers</title>
<style>
  :root{ --fg:#1a1a1a; --mut:#6b7280; --line:#e5e7eb; --bg:#fff; --card:#fafafa; --accent:#2563eb; --icon:#1a1a1a; }
  *{box-sizing:border-box;}
  body{font-family:system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;color:var(--fg);background:var(--bg);margin:0;padding:32px 40px 80px;}
  h1{font-size:22px;font-weight:600;margin:0 0 6px;}
  .sub{color:var(--mut);font-size:14px;line-height:1.6;} .sub code{background:var(--card);padding:2px 6px;border-radius:4px;font-size:13px;} .sub b{color:var(--fg);} .sub a{color:var(--accent);text-decoration:none;}
  .toolbar{position:sticky;top:0;background:var(--bg);padding:14px 0;border-bottom:1px solid var(--line);margin:18px 0 14px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;z-index:5;}
  #q{flex:1;min-width:200px;padding:10px 14px;font-size:14px;border:1px solid var(--line);border-radius:8px;outline:none;} #q:focus{border-color:var(--accent);}
  .chips button{font-size:13px;padding:7px 12px;border:1px solid var(--line);background:var(--bg);border-radius:7px;cursor:pointer;color:var(--fg);margin-right:6px;}
  .chips button.on{background:var(--fg);color:#fff;border-color:var(--fg);}
  .stat{font-size:13px;color:var(--mut);}
  .palette{display:flex;gap:8px;align-items:center;padding:10px 0 4px;flex-wrap:wrap;}
  .palette .lbl{font-size:13px;color:var(--mut);margin-right:2px;}
  .sw{width:24px;height:24px;border-radius:6px;cursor:pointer;border:1px solid rgba(0,0,0,.12);} .sw.on{outline:2px solid var(--accent);outline-offset:1px;}
  .palette input[type=color]{width:30px;height:26px;border:1px solid var(--line);border-radius:6px;background:none;cursor:pointer;padding:0;}
  section.cat{margin-bottom:32px;}
  h2{font-size:15px;font-weight:600;margin:0 0 14px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;}
  .cnt{font-size:12px;font-weight:500;color:var(--mut);background:var(--card);border:1px solid var(--line);border-radius:20px;padding:1px 9px;}
  .badge{font-size:11px;font-weight:400;color:var(--mut);}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));gap:12px;}
  .cell{position:relative;border:1px solid var(--line);border-radius:10px;background:var(--card);padding:16px 8px 10px;text-align:center;cursor:pointer;transition:all .12s;}
  .cell:hover{border-color:var(--accent);background:#fff;transform:translateY(-2px);}
  .ic{height:32px;display:flex;align-items:center;justify-content:center;} .ic svg{width:30px;height:30px;}
  .colorable .ic svg{color:var(--icon);}
  .nm{margin-top:9px;font-size:10.5px;color:var(--mut);word-break:break-all;font-family:ui-monospace,Menlo,monospace;line-height:1.3;}
  .tag{position:absolute;top:6px;right:6px;font-size:9px;color:#aaa;}
  .acts{position:absolute;top:5px;left:5px;display:none;gap:3px;} .cell:hover .acts{display:flex;}
  .act{font-size:9px;padding:2px 5px;border:1px solid var(--line);background:#fff;border-radius:4px;cursor:pointer;color:var(--mut);line-height:1.4;} .act:hover{border-color:var(--accent);color:var(--accent);}
  .cell.hide,.cat.hide{display:none;}
  #toast{position:fixed;bottom:26px;left:50%;transform:translateX(-50%) translateY(20px);background:var(--fg);color:#fff;padding:10px 18px;border-radius:8px;font-size:13px;opacity:0;transition:all .2s;pointer-events:none;} #toast.show{opacity:1;transform:translateX(-50%) translateY(0);}
</style></head>
<body>
  <h1>ML Paper Icons</h1>
  <div class="sub"><b>__TOTAL__</b> free vector icons for AI / ML / multimodal / LLM / NLP / Agent papers · mono <b>Lucide __ML__ · Tabler __MT__ · Phosphor __MP__</b> (recolorable) + color <b>brand logos __CB__ · duotone __CD__</b> · all MIT/ISC, commercial-safe, no attribution required · <a href="https://github.com/YOUR_NAME/ml-paper-icons">GitHub</a><br><b>Click</b> = copy SVG, hover for <b>PNG</b> / <b>download</b>. Mono icons default to black; use the palette below to recolor (copied SVG/PNG keeps the color).</div>
  <div class="palette">
    <span class="lbl">recolor mono:</span>
    <span class="sw" style="background:#1a1a1a" data-c="#1a1a1a" onclick="setColor(this)"></span>
    <span class="sw" style="background:#6BAED6" data-c="#6BAED6" onclick="setColor(this)"></span>
    <span class="sw" style="background:#27AE60" data-c="#27AE60" onclick="setColor(this)"></span>
    <span class="sw" style="background:#E74C3C" data-c="#E74C3C" onclick="setColor(this)"></span>
    <span class="sw" style="background:#F39C12" data-c="#F39C12" onclick="setColor(this)"></span>
    <span class="sw" style="background:#8E44AD" data-c="#8E44AD" onclick="setColor(this)"></span>
    <span class="sw" style="background:#185FA5" data-c="#185FA5" onclick="setColor(this)"></span>
    <input type="color" value="#1a1a1a" oninput="setColorVal(this.value)" title="custom color">
  </div>
  <div class="toolbar">
    <input id="q" placeholder="search: robot / openai / attention / audio ..." oninput="filter()" autofocus>
    <div class="chips">
      <button class="on" data-f="all" onclick="setLib(this)">All</button>
      <button data-f="brand" onclick="setLib(this)">Brand</button>
      <button data-f="duotone" onclick="setLib(this)">Duotone</button>
      <button data-f="lucide" onclick="setLib(this)">Lucide</button>
      <button data-f="tabler" onclick="setLib(this)">Tabler</button>
      <button data-f="phosphor" onclick="setLib(this)">Phosphor</button>
    </div>
    <div class="stat" id="stat"></div>
  </div>
  __SECTIONS__
  <div id="toast"></div>
<script>
var curLib='all';
function apply(){
  var q=document.getElementById('q').value.trim().toLowerCase();var shown=0;
  document.querySelectorAll('.cell').forEach(function(c){
    var m=(c.dataset.name.indexOf(q)!==-1)&&(curLib==='all'||c.dataset.lib===curLib);
    c.classList.toggle('hide',!m);if(m)shown++;
  });
  document.querySelectorAll('.cat').forEach(function(s){s.classList.toggle('hide',s.querySelectorAll('.cell:not(.hide)').length===0);});
  document.getElementById('stat').textContent=shown+' shown';
}
function filter(){apply();}
function setLib(b){curLib=b.dataset.f;document.querySelectorAll('.chips button').forEach(function(x){x.classList.remove('on');});b.classList.add('on');apply();}
function setColor(el){document.querySelectorAll('.sw').forEach(function(s){s.classList.remove('on');});el.classList.add('on');setColorVal(el.dataset.c);}
function setColorVal(v){document.documentElement.style.setProperty('--icon',v);}
function toast(msg){var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){t.classList.remove('show');},1500);}
function curIconColor(){return getComputedStyle(document.documentElement).getPropertyValue('--icon').trim()||'#1a1a1a';}
function svgStr(cell,px){
  var svg=cell.querySelector('.ic svg').cloneNode(true);
  svg.setAttribute('xmlns','http://www.w3.org/2000/svg');
  if(cell.classList.contains('colorable')){
    var col=curIconColor();
    svg.setAttribute('color',col);
    svg.querySelectorAll('[stroke]').forEach(function(n){if(n.getAttribute('stroke')!=='none')n.setAttribute('stroke',col);});
    svg.querySelectorAll('[fill]').forEach(function(n){var f=n.getAttribute('fill');if(f&&f!=='none'&&f!=='currentColor')n.setAttribute('fill',col);});
  }
  if(px){svg.setAttribute('width',px);svg.setAttribute('height',px);}
  return new XMLSerializer().serializeToString(svg);
}
function copySVG(cell){navigator.clipboard.writeText(svgStr(cell)).then(function(){toast('Copied SVG: '+cell.dataset.name);},function(){toast('Copy failed');});}
function copyPNG(btn){
  var cell=btn.closest('.cell');var s=svgStr(cell,256);var img=new Image();
  var url=URL.createObjectURL(new Blob([s],{type:'image/svg+xml;charset=utf-8'}));
  img.onload=function(){var c=document.createElement('canvas');c.width=256;c.height=256;c.getContext('2d').drawImage(img,0,0,256,256);URL.revokeObjectURL(url);
    c.toBlob(function(blob){if(navigator.clipboard&&window.ClipboardItem){navigator.clipboard.write([new ClipboardItem({'image/png':blob})]).then(function(){toast('Copied PNG: '+cell.dataset.name);},function(){toast('PNG copy failed, use download');});}else{toast('PNG copy unsupported, use download');}});};
  img.onerror=function(){toast('render failed');};img.src=url;
}
function dl(btn){var cell=btn.closest('.cell');var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([svgStr(cell)],{type:'image/svg+xml'}));a.download=cell.dataset.name+'.svg';a.click();URL.revokeObjectURL(a.href);toast('Downloaded: '+cell.dataset.name+'.svg');}
apply();
</script>
</body></html>'''

html = (TEMPLATE.replace("__TOTAL__", str(total)).replace("__ML__", str(ml))
        .replace("__MT__", str(mt)).replace("__MP__", str(mp))
        .replace("__CB__", str(cb)).replace("__CD__", str(cd))
        .replace("__SECTIONS__", "".join(sections)))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print(f"wrote {OUT}  total={total}")
