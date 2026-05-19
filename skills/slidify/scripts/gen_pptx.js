#!/usr/bin/env node
/**
 * gen_pptx.js — Slidify Generator
 * Usage: node scripts/gen_pptx.js [slides.json]
 *
 * Reads a slide spec JSON + template config, generates a .pptx file.
 * Edit slides.json (the spec), not this file.
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// ─── Load args ────────────────────────────────────────────────────────────────
const specPath = process.argv[2] || "slides.json";
const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
const meta = spec.meta || {};

// ─── Load template ────────────────────────────────────────────────────────────
const TEMPLATES_DIR = path.join(__dirname, "..", "assets", "templates");
let template = loadTemplate(meta.template || "default");

function loadTemplate(name) {
  const tpath = path.join(TEMPLATES_DIR, `${name}.json`);
  if (!fs.existsSync(tpath)) {
    console.warn(`Template "${name}" not found, using default`);
    return loadTemplate("default");
  }
  const t = JSON.parse(fs.readFileSync(tpath, "utf8"));
  if (t.extends) {
    const base = loadTemplate(t.extends);
    return deepMerge(base, t);
  }
  return t;
}

function deepMerge(base, override) {
  const result = { ...base };
  for (const key of Object.keys(override)) {
    if (typeof override[key] === "object" && !Array.isArray(override[key]) &&
        override[key] !== null && typeof base[key] === "object") {
      result[key] = deepMerge(base[key], override[key]);
    } else {
      result[key] = override[key];
    }
  }
  return result;
}

// ─── Color helpers ────────────────────────────────────────────────────────────
const P = template.palette || {};
function col(key) {
  const v = P[key] || key || "000000";
  return v.replace(/^#/, "");
}

// ─── Presentation setup ───────────────────────────────────────────────────────
const pres = new pptxgen();
pres.layout = {
  "16x9": "LAYOUT_16x9", "16x10": "LAYOUT_16x10",
  "4x3": "LAYOUT_4x3",   "wide": "LAYOUT_WIDE"
}[meta.layout || "16x9"] || "LAYOUT_16x9";

pres.title  = meta.title  || "Presentation";
pres.author = meta.author || "";

const SW = 10, SH = 5.625;
const slides = spec.slides || [];
const total  = slides.length;

// ─── Helpers ──────────────────────────────────────────────────────────────────
const makeShadow = () => ({
  type: "outer", color: "000000", opacity: 0.10, blur: 6, offset: 2, angle: 135
});

async function addWatermark(slide, slideType, slideOverride) {
  if (slideOverride?.watermark?.enabled === false) return;
  const wconfig = slideOverride?.watermark || template.watermark || {};
  const wmArr = template.watermarks ? template.watermarks : (wconfig.enabled ? [wconfig] : []);
  for (const wm of wmArr) {
    if (!wm.enabled && !template.watermarks) continue;
    const skipTypes = wm.skip_slide_types || [];
    if (skipTypes.includes(slideType)) continue;
    const {
      type="image", path: imgPath, text,
      position="bottom-right", opacity=15, w=0.9, h=0.9, margin=0.2,
      rotate=0, fontSize=48, color="AAAAAA", bold=false
    } = wm;
    const transparency = 100 - opacity;
    const pos = resolvePos(position, w, h, margin);
    if (type === "image" && imgPath) {
      if (!fs.existsSync(imgPath)) { console.warn(`Watermark image not found: ${imgPath}`); continue; }
      slide.addImage({ path: imgPath, ...pos, w, h, transparency });
    } else if (type === "text" && text) {
      slide.addText(text, {
        ...pos, w: w || 6, h: h || 1.5,
        fontSize, color: col(color), bold,
        rotate, transparency, align: "center"
      });
    }
  }
}

function resolvePos(pos, w, h, margin) {
  const m = margin;
  const positions = {
    "bottom-right":  { x: SW-w-m, y: SH-h-m },
    "bottom-left":   { x: m,      y: SH-h-m },
    "top-right":     { x: SW-w-m, y: m       },
    "top-left":      { x: m,      y: m       },
    "bottom-center": { x: (SW-w)/2, y: SH-h-m },
    "center":        { x: (SW-w)/2, y: (SH-h)/2 }
  };
  return positions[pos] || positions["bottom-right"];
}

function addFooter(slide, slideNum, slideType, slideOverride) {
  const fc = slideOverride?.footer !== undefined ? slideOverride.footer : template.footer;
  if (!fc || !fc.enabled) return;
  const skipOn = fc.skip_slide_types || [];
  if (skipOn.includes(slideType)) return;
  const { left="", center="", right="", color="9CA3AF", fontSize=9, y=5.3 } = fc;
  const fmt = str => (str||"")
    .replace("{n}", slideNum).replace("{total}", total)
    .replace("{title}", pres.title).replace("{author}", pres.author)
    .replace("{date}", meta.date || new Date().getFullYear().toString());
  if (left)   slide.addText(fmt(left),   { x:0.3, y, w:3,   h:0.25, fontSize, color:col(color), align:"left",   margin:0 });
  if (center) slide.addText(fmt(center), { x:3.5, y, w:3,   h:0.25, fontSize, color:col(color), align:"center", margin:0 });
  if (right)  slide.addText(fmt(right),  { x:7,   y, w:2.7, h:0.25, fontSize, color:col(color), align:"right",  margin:0 });
}

// ─── Slide renderers ──────────────────────────────────────────────────────────

async function renderTitleSlide(slide, s) {
  const tc = template.title_slide || {};
  const bg = tc.bg === "dark_bg" ? col("dark_bg") : col("bg");
  slide.background = { color: bg };
  const textColor = bg === col("bg") ? col("text") : "FFFFFF";
  const accentColor = col("accent");
  slide.addText(s.title || "", {
    x: 0.8, y: 1.5, w: 8.4, h: 1.5,
    fontSize: 40, fontFace: template.fonts?.title || "Calibri",
    bold: true, color: textColor, align: "center", valign: "middle"
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 3.5, y: 3.15, w: 3, h: 0.04, fill: { color: accentColor }
  });
  if (s.subtitle) {
    slide.addText(s.subtitle, {
      x: 1, y: 3.3, w: 8, h: 0.5,
      fontSize: 16, color: textColor, align: "center", italic: true
    });
  }
  const infoLines = [s.presenter, s.affiliation, s.date].filter(Boolean);
  if (infoLines.length) {
    slide.addText(infoLines.join("  \u00b7  "), {
      x: 1, y: 4.2, w: 8, h: 0.4,
      fontSize: 12, color: col("muted") !== "muted" ? col("muted") : "9CA3AF",
      align: "center"
    });
  }
}

async function renderSectionSlide(slide, s) {
  slide.background = { color: col("dark_bg") };
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.8, y: 2.4, w: 0.06, h: 1.2, fill: { color: col("accent") }
  });
  slide.addText(s.title || "", {
    x: 1.1, y: 2.3, w: 8, h: 1.0,
    fontSize: 36, bold: true, color: "FFFFFF",
    fontFace: template.fonts?.title || "Calibri"
  });
  if (s.subtitle) {
    slide.addText(s.subtitle, {
      x: 1.1, y: 3.4, w: 7.5, h: 0.5,
      fontSize: 15, color: "CBD5E1", italic: true
    });
  }
}

async function renderBullets(slide, s) {
  const items = s.items || [];
  slide.addText(
    items.map((item, i) => ({
      text: item,
      options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 6 }
    })),
    { x: 0.6, y: 1.35, w: 8.8, h: 3.8, fontSize: 18, color: col("text"), fontFace: template.fonts?.body || "Calibri" }
  );
}

async function renderStats(slide, s) {
  const stats = s.stats || [];
  const count = Math.min(stats.length, 4);
  const cellW = SW / count;
  stats.slice(0, count).forEach((stat, i) => {
    const cx = i * cellW + cellW / 2 - 2;
    slide.addText(stat.value, { x: cx, y: 1.6, w: 4, h: 1.3, fontSize: 60, bold: true, color: col("primary"), align: "center", fontFace: template.fonts?.title || "Calibri" });
    slide.addText(stat.label || "", { x: cx, y: 3.1, w: 4, h: 0.5, fontSize: 13, color: col("muted") !== "muted" ? col("muted") : "6B7280", align: "center" });
    if (i < count - 1) {
      slide.addShape(pres.shapes.LINE, { x: (i+1) * cellW, y: 1.5, w: 0, h: 2.2, line: { color: "E2E8F0", width: 1 } });
    }
  });
}

async function renderChart(slide, s) {
  const c = s.chart || {};
  const typeMap = { bar: pres.charts.BAR, column: pres.charts.BAR, line: pres.charts.LINE, pie: pres.charts.PIE, doughnut: pres.charts.DOUGHNUT, area: pres.charts.AREA, scatter: pres.charts.SCATTER };
  const chartType = typeMap[c.kind] || pres.charts.BAR;
  const data = (c.series || []).map(s => ({ name: s.name, labels: c.labels || [], values: s.values || [] }));
  const colors = c.colors || [col("primary"), col("accent"), "64748B", "94A3B8"];
  slide.addChart(chartType, data, {
    x: 0.5, y: 1.2, w: 9, h: 4, barDir: c.kind === "bar" ? "bar" : "col",
    chartColors: colors, chartArea: { fill: { color: "FFFFFF" } },
    catAxisLabelColor: "64748B", valAxisLabelColor: "64748B",
    valGridLine: { color: "E2E8F0", size: 0.5 }, catGridLine: { style: "none" },
    showValue: c.showValues !== false, dataLabelColor: col("text"),
    showLegend: data.length > 1, legendPos: "b", title: c.title, showTitle: !!c.title
  });
}

async function renderCards(slide, s) {
  const cards = s.cards || [];
  const count = Math.min(cards.length, 4);
  const colCount = count <= 2 ? count : Math.min(count, 4);
  const cardW = (SW - 0.8) / colCount - 0.2;
  cards.slice(0, colCount).forEach((card, i) => {
    const x = 0.4 + i * (cardW + 0.2), y = 1.3, h = 3.5;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cardW, h, fill: { color: "F8FAFC" }, line: { color: "E2E8F0", width: 1 }, shadow: makeShadow(), rectRadius: 0.08 });
    slide.addShape(pres.shapes.RECTANGLE, { x, y, w: cardW, h: 0.06, fill: { color: col("accent") } });
    slide.addText(card.title || "", { x: x + 0.15, y: y + 0.2, w: cardW - 0.3, h: 0.5, fontSize: 14, bold: true, color: col("primary"), margin: 0 });
    slide.addText(card.body || "", { x: x + 0.15, y: y + 0.85, w: cardW - 0.3, h: 2.4, fontSize: 12, color: col("text"), margin: 0 });
  });
}

async function renderTimeline(slide, s) {
  const steps = s.steps || [];
  const count = steps.length;
  const stepW = (SW - 1.2) / count;
  const lineY = 2.8;
  slide.addShape(pres.shapes.LINE, { x: 0.6, y: lineY, w: SW - 1.2, h: 0, line: { color: col("accent"), width: 2 } });
  steps.forEach((step, i) => {
    const cx = 0.6 + i * stepW + stepW / 2;
    slide.addShape(pres.shapes.OVAL, { x: cx - 0.18, y: lineY - 0.18, w: 0.36, h: 0.36, fill: { color: col("primary") }, line: { color: col("accent"), width: 2 } });
    slide.addText(step.label || "", { x: cx - stepW/2 + 0.1, y: lineY - 0.9, w: stepW - 0.2, h: 0.4, fontSize: 11, bold: true, color: col("accent"), align: "center", margin: 0 });
    slide.addText(step.text || "", { x: cx - stepW/2 + 0.1, y: lineY + 0.35, w: stepW - 0.2, h: 1.0, fontSize: 12, color: col("text"), align: "center" });
  });
}

async function renderClosing(slide, s) {
  slide.background = { color: col("dark_bg") };
  slide.addText(s.title || "Thank You", { x: 1, y: 1.2, w: 8, h: 1.2, fontSize: 44, bold: true, color: "FFFFFF", align: "center", fontFace: template.fonts?.title || "Calibri" });
  if (s.contact) slide.addText(s.contact, { x: 1, y: 2.6, w: 8, h: 0.4, fontSize: 14, color: col("accent"), align: "center" });
  if (s.links?.length) {
    slide.addText(s.links.map(l => l.label).join("   \u00b7   "), { x: 1, y: 3.2, w: 8, h: 0.4, fontSize: 12, color: "94A3B8", align: "center" });
  }
  if (s.shapes) await renderShapes(slide, s.shapes);
}

async function renderShapes(slide, shapes) {
  for (const sh of shapes) {
    if (sh.type === "rect") {
      const opts = { x: sh.x, y: sh.y, w: sh.w === "100%" ? SW : sh.w, h: sh.h === "100%" ? SH : sh.h };
      if (sh.fill && sh.fill.type !== "none") opts.fill = { color: sh.fill.color || col("bg") };
      else opts.fill = { type: "none" };
      if (sh.line) opts.line = { color: sh.line.color, width: sh.line.width || 1 };
      slide.addShape(pres.shapes.RECTANGLE, opts);
    } else if (sh.type === "text") {
      const opts = {
        x: sh.x, y: sh.y, w: sh.w, h: sh.h,
        fontSize: sh.fontSize || 14,
        fontFace: sh.fontFace || template.fonts?.title || "Calibri",
        color: sh.color || "FFFFFF",
        bold: !!sh.bold,
        align: sh.align || "left",
        valign: sh.valign || "top",
        margin: 0
      };
      if (sh.lineSpacingMultiple) opts.lineSpacingMultiple = sh.lineSpacingMultiple;
      slide.addText(sh.text || "", opts);
    }
  }
}

async function renderContentSlide(slide, s) {
  slide.addText(s.title || "", { x: 0.5, y: 0.25, w: 9, h: 0.75, fontSize: 28, bold: true, color: col("primary"), fontFace: template.fonts?.title || "Calibri", margin: 0 });
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.05, w: 9, h: 0.03, fill: { color: col("accent") } });
  const layout = s.layout || "bullets";
  switch (layout) {
    case "bullets":     await renderBullets(slide, s); break;
    case "stats":       await renderStats(slide, s);   break;
    case "chart":       await renderChart(slide, s);   break;
    case "cards":       await renderCards(slide, s);   break;
    case "timeline":    await renderTimeline(slide, s); break;
    case "two-column":  await renderTwoColumn(slide, s); break;
    case "image-right": await renderImageSide(slide, s, "right"); break;
    case "image-left":  await renderImageSide(slide, s, "left"); break;
    case "blank": break;
    default: if (s.items) await renderBullets(slide, s);
  }
}

async function renderTwoColumn(slide, s) {
  await renderBlock(slide, s.left,  { x: 0.5, y: 1.3, w: 4.5, h: 4.0 });
  await renderBlock(slide, s.right, { x: 5.2, y: 1.3, w: 4.5, h: 4.0 });
}

async function renderImageSide(slide, s, imgSide) {
  const imgX = imgSide === "right" ? 5.8 : 0.5;
  const textX = imgSide === "right" ? 0.5 : 5.8;
  if (s.image?.path || s.path) {
    const p = s.image?.path || s.path;
    if (fs.existsSync(p)) slide.addImage({ path: p, x: imgX, y: 1.3, w: 3.8, h: 3.8, sizing: { type:"contain", w:3.8, h:3.8 } });
  }
  if (s.items) {
    slide.addText(s.items.map((item, i) => ({ text: item, options: { bullet: true, breakLine: i < s.items.length - 1, paraSpaceAfter: 6 } })), { x: textX, y: 1.3, w: 4.0, h: 3.8, fontSize: 16, color: col("text") });
  }
}

async function renderBlock(slide, block, bounds) {
  if (!block) return;
  const { x, y, w, h } = bounds;
  switch (block.type) {
    case "bullets":
      slide.addText((block.items || []).map((item, i, arr) => ({ text: item, options: { bullet: true, breakLine: i < arr.length - 1, paraSpaceAfter: 4 } })), { x, y, w, h, fontSize: 15, color: col("text") });
      break;
    case "text":
      slide.addText(block.content || "", { x, y, w, h, fontSize: 15, color: col("text") });
      break;
    case "image":
      if (block.path && fs.existsSync(block.path)) slide.addImage({ path: block.path, x, y, w, h, sizing: { type:"contain", w, h } });
      break;
    case "stats":
      (block.stats || []).forEach((stat, i) => {
        const sy = y + i * 1.1;
        slide.addText(stat.value, { x, y: sy, w, h: 0.7, fontSize: 36, bold: true, color: col("primary"), align: "center", margin: 0 });
        slide.addText(stat.label, { x, y: sy + 0.7, w, h: 0.35, fontSize: 11, color: col("muted") !== "muted" ? col("muted") : "6B7280", align: "center", margin: 0 });
      });
      break;
  }
}

// ─── Main render loop ─────────────────────────────────────────────────────────
(async () => {
  for (let i = 0; i < slides.length; i++) {
    const s = slides[i];
    const slideNum = i + 1;
    const override = s._template_override || {};
    const slide = pres.addSlide();
    slide.background = { color: col("bg") };

    switch (s.type) {
      case "title":      await renderTitleSlide(slide, s);   break;
      case "section":    await renderSectionSlide(slide, s); break;
      case "content":    await renderContentSlide(slide, s); break;
      case "closing":    await renderClosing(slide, s);      break;
      case "blank":
        if (s.shapes) await renderShapes(slide, s.shapes);
        break;
      case "image-full":
        if (s.path && fs.existsSync(s.path)) {
          slide.background = { path: s.path };
          if (s.caption) slide.addText(s.caption, { x:0.5, y:5.0, w:9, h:0.4, fontSize:11, color:"FFFFFF", align:"center" });
        }
        break;
      default: await renderContentSlide(slide, s);
    }

    const noFooterTypes = template.title_slide?.show_footer === false ? ["title"] : [];
    const noFooterTypes2 = template.closing_slide?.show_footer === false ? ["closing"] : noFooterTypes;
    const actualNoFooter = [...new Set([...noFooterTypes2, ...((template.footer?.skip_slide_types)||[])])];
    if (!actualNoFooter.includes(s.type)) addFooter(slide, slideNum, s.type, override);
    await addWatermark(slide, s.type, override);
    if (s.notes) slide.addNotes(s.notes);
  }

  const outPath = meta.output || "output.pptx";
  await pres.writeFile({ fileName: outPath });
  console.log(`Saved: ${outPath} (${slides.length} slides)`);
})();
