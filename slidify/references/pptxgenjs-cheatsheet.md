# pptxGenJS Cheatsheet

Condensed API for generated code. For full docs: https://gitbrent.github.io/PptxGenJS/

## Setup

```javascript
const pptxgen = require("pptxgenjs");
let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";   // 10" x 5.625"
// LAYOUT_16x10 | LAYOUT_4x3 | LAYOUT_WIDE (13.3x7.5")
```

## Slide

```javascript
let slide = pres.addSlide();
slide.background = { color: "1E3A5F" };           // solid
slide.background = { path: "assets/bg.jpg" };     // image
slide.background = { data: "image/png;base64,..." }; // base64
```

## Text

```javascript
slide.addText("Title", {
  x: 0.5, y: 0.3, w: 9, h: 0.8,
  fontSize: 40, fontFace: "Calibri", bold: true,
  color: "FFFFFF", align: "center", valign: "middle",
  margin: 0    // remove internal padding for precise alignment
});

// Rich text
slide.addText([
  { text: "Bold ", options: { bold: true } },
  { text: "normal" }
], { x: 1, y: 1, w: 8, h: 1 });

// Multi-line
slide.addText([
  { text: "Line 1", options: { breakLine: true } },
  { text: "Line 2" }
], { x: 1, y: 1, w: 8, h: 2 });
```

## Bullets

```javascript
// CORRECT: use bullet: true
slide.addText([
  { text: "First",  options: { bullet: true, breakLine: true } },
  { text: "Second", options: { bullet: true, breakLine: true } },
  { text: "Third",  options: { bullet: true } }
], { x: 0.5, y: 1, w: 9, h: 3, fontSize: 16 });

// WRONG: never use unicode bullet character
```

## Shapes

```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 4.9, w: 10, h: 0.725,
  fill: { color: "1E3A5F" }
});

slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1, y: 1, w: 3, h: 1.5,
  fill: { color: "FFFFFF" },
  shadow: makeShadow()   // always use factory, not shared object
});

const makeShadow = () => ({
  type: "outer", color: "000000", opacity: 0.12,
  blur: 6, offset: 2, angle: 135
});
```

## Images

```javascript
slide.addImage({ path: "assets/logo.png", x: 8.8, y: 4.6, w: 0.9, h: 0.9 });
slide.addImage({ data: "image/png;base64,...", x: 1, y: 1, w: 4, h: 3 });

// Opacity (for watermark effect)
slide.addImage({
  path: "assets/logo.png",
  x: 8.8, y: 4.6, w: 0.9, h: 0.9,
  transparency: 80   // 0=opaque, 100=invisible; for 15% opacity -> transparency: 85
});
```

**Watermark opacity formula:** `transparency = 100 - desired_opacity`
- Want 15% visible -> `transparency: 85`
- Want 20% visible -> `transparency: 80`
- Want 25% visible -> `transparency: 75`

## Charts (native)

```javascript
slide.addChart(pres.charts.BAR, [
  { name: "Series", labels: ["A","B","C"], values: [10, 20, 15] }
], {
  x: 0.5, y: 1, w: 9, h: 4, barDir: "col",
  chartColors: ["2563EB"],
  chartArea: { fill: { color: "FFFFFF" } },
  catAxisLabelColor: "64748B",
  valAxisLabelColor: "64748B",
  valGridLine: { color: "E2E8F0", size: 0.5 },
  catGridLine: { style: "none" },
  showValue: true, dataLabelColor: "1E293B",
  showLegend: false
});

// Chart types: BAR, LINE, PIE, DOUGHNUT, AREA, SCATTER, BUBBLE, RADAR
```

## Footer Helper

```javascript
function addFooter(slide, pres, slideNum, totalSlides, config) {
  const { left="", center="", right="", color="9CA3AF", fontSize=9, y=5.3 } = config;
  const fmt = str => str
    .replace("{n}", slideNum).replace("{total}", totalSlides)
    .replace("{title}", pres.title || "");

  if (left)   slide.addText(fmt(left),   { x:0.3, y, w:3,   h:0.25, fontSize, color, align:"left",   margin:0 });
  if (center) slide.addText(fmt(center), { x:3.5, y, w:3,   h:0.25, fontSize, color, align:"center", margin:0 });
  if (right)  slide.addText(fmt(right),  { x:7,   y, w:2.7, h:0.25, fontSize, color, align:"right",  margin:0 });
}
```

## Watermark Helper

```javascript
async function addWatermark(slide, config) {
  if (!config.enabled) return;
  const { path, position="bottom-right", opacity=15, w=0.9, h=0.9, margin=0.2 } = config;
  const transparency = 100 - opacity;
  const pos = resolvePosition(position, w, h, margin);
  slide.addImage({ path, ...pos, w, h, transparency });
}

function resolvePosition(pos, w, h, margin) {
  const SW=10, SH=5.625;
  const positions = {
    "bottom-right":  { x: SW-w-margin, y: SH-h-margin },
    "bottom-left":   { x: margin,      y: SH-h-margin },
    "top-right":     { x: SW-w-margin, y: margin       },
    "top-left":      { x: margin,      y: margin       },
    "bottom-center": { x: (SW-w)/2,    y: SH-h-margin  },
    "center":        { x: (SW-w)/2,    y: (SH-h)/2     }
  };
  return positions[pos] || positions["bottom-right"];
}
```

## Save

```javascript
await pres.writeFile({ fileName: "output.pptx" });
// or in-memory:
const data = await pres.write({ outputType: "nodebuffer" });
```

## Critical: Never Do These

```javascript
color: "#FF0000"           // no # prefix
"00000020"                 // 8-char hex for opacity
"•" in text               // use bullet: true
shared shadow object       // use factory () => ({...})
slide.addImage data URLs   // no data: URL scheme; use "image/png;base64,..."
```
