#!/usr/bin/env node
/**
 * add_animations.js — Slidify Animation Post-Processor
 *
 * Usage: node scripts/add_animations.js <pptx-file> <animations.json> [output-file]
 *
 * Injects OOXML animation/transition XML into a PPTX file.
 * PptxGenJS has no animation support, so this script post-processes the ZIP.
 *
 * animations.json schema:
 * {
 *   "transitions": {
 *     "default": { "type": "fade", "speed": "med", "advanceOnClick": true },
 *     "1": { "type": "push", "direction": "l", "speed": "fast" },
 *     "5": { "type": "zoom", "speed": "med" }
 *   },
 *   "animations": {
 *     "1": [
 *       { "target": 0, "effect": "fadeIn", "duration": 800, "trigger": "withPrev" },
 *       { "target": 1, "effect": "flyIn", "direction": "b", "duration": 600, "trigger": "afterPrev", "delay": 200 }
 *     ]
 *   }
 * }
 *
 * target: 0-based index of elements in the order they were added to the slide
 *         (title text = 0, accent line = 1, body = 2, etc.)
 */

const fs = require("fs");
const path = require("path");
const JSZip = require("jszip");

// ─── Animation XML generators ────────────────────────────────────────────────

const SPEED_MAP = { slow: "slow", med: "med", fast: "fast" };

function transitionXml(config) {
  const { type = "fade", speed = "med", direction, orient, spokes, advanceOnClick = true, advanceTime = 0 } = config;
  const spd = SPEED_MAP[speed] || "med";
  const advClick = advanceOnClick ? "1" : "0";
  const advTm = advanceTime || "0";

  let inner = "";
  switch (type) {
    case "fade":     inner = "<p:fade/>"; break;
    case "push":     inner = `<p:push dir="${dir(direction, "l")}"/>`; break;
    case "cover":    inner = `<p:cover dir="${dir(direction, "l")}"/>`; break;
    case "uncover":  inner = `<p:uncover dir="${dir(direction, "l")}"/>`; break;
    case "wipe":     inner = `<p:wipe dir="${dir(direction, "l")}"/>`; break;
    case "split":    inner = `<p:split orient="${orient || "horiz"}" dir="${dir(direction, "in")}"/>`; break;
    case "zoom":     inner = "<p:zoom/>"; break;
    case "cut":      inner = "<p:cut/>"; break;
    case "dissolve": inner = "<p:dissolve/>"; break;
    case "blinds":   inner = `<p:blinds orient="${orient || "horiz"}"/>`; break;
    case "checker":  inner = `<p:checker dir="${dir(direction, "l")}"/>`; break;
    case "circle":   inner = "<p:circle/>"; break;
    case "diamond":  inner = "<p:diamond/>"; break;
    case "newsflash":inner = "<p:newsflash/>"; break;
    case "plus":     inner = "<p:plus/>"; break;
    case "wedge":    inner = "<p:wedge/>"; break;
    case "wheel":    inner = `<p:wheel spokes="${spokes || 4}"/>`; break;
    case "random":   inner = "<p:random/>"; break;
    case "flyThrough":inner = `<p:flyThrough dir="${dir(direction, "l")}"/>`; break;
    case "gallery":  inner = "<p:gallery/>"; break;
    case "convey":   inner = "<p:convey/>"; break;
    case "pan":      inner = `<p:pan dir="${dir(direction, "l")}"/>`; break;
    case "glitter":  inner = `<p:glitter dir="${dir(direction, "l")}"/>`; break;
    case "vortex":   inner = "<p:vortex/>"; break;
    case "switch":   inner = `<p:switch dir="${dir(direction, "l")}"/>`; break;
    case "flip":     inner = `<p:flip dir="${dir(direction, "l")}"/>`; break;
    case "fall":     inner = "<p:fall/>"; break;
    case "fracture": inner = "<p:fracture/>"; break;
    case "crush":    inner = "<p:crush/>"; break;
    case "peelOff":  inner = "<p:peelOff/>"; break;
    default:         inner = "<p:fade/>";
  }

  return `<p:transition spd="${spd}" advClick="${advClick}" advTm="${advTm}">${inner}</p:transition>`;
}

function dir(d, fallback) {
  const valid = { l: "l", r: "r", t: "t", b: "b", left: "l", right: "r", top: "t", bottom: "b", in: "in", out: "out" };
  return valid[d] || fallback;
}

// ─── Effect XML builders ─────────────────────────────────────────────────────

function buildEffectXml(effect, spid, duration, delay, direction) {
  const dur = duration || 1000;
  const del = delay || 0;

  switch (effect) {
    case "fadeIn":
      return fadeInXml(spid, dur, del);
    case "fadeOut":
      return fadeOutXml(spid, dur, del);
    case "flyIn":
      return flyInXml(spid, dur, del, direction);
    case "flyOut":
      return flyOutXml(spid, dur, del, direction);
    case "wipe":
      return wipeInXml(spid, dur, del, direction);
    case "zoom":
      return zoomInXml(spid, dur, del);
    case "floatIn":
      return floatInXml(spid, dur, del, direction);
    case "floatOut":
      return floatOutXml(spid, dur, del, direction);
    case "split":
      return splitInXml(spid, dur, del, direction);
    case "blinds":
      return blindsInXml(spid, dur, del, direction);
    case "box":
      return boxInXml(spid, dur, del, direction);
    case "dissolve":
      return dissolveInXml(spid, dur, del);
    case "expand":
      return expandInXml(spid, dur, del);
    case "growAndTurn":
      return growAndTurnXml(spid, dur, del);
    case "swivel":
      return swivelXml(spid, dur, del);
    case "pulse":
      return pulseXml(spid, dur, del);
    case "spin":
      return spinXml(spid, dur, del, direction);
    case "grow":
      return scaleXml(spid, dur, del, "125000");
    case "shrink":
      return scaleXml(spid, dur, del, "75000");
    case "teeter":
      return teeterXml(spid, dur, del);
    case "blink":
      return blinkXml(spid, dur, del);
    default:
      return fadeInXml(spid, dur, del);
  }
}

function fadeInXml(spid, dur, del) {
  return `<p:set><p:cBhvr><p:cTn id="5" dur="1" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:anim><p:cBhvr><p:cTn id="6" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.opacity</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst><p:tav tm="0"><p:val><p:strVal val="0"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="1"/></p:val></p:tav></p:tavLst></p:anim>`;
}

function fadeOutXml(spid, dur, del) {
  return `<p:anim><p:cBhvr><p:cTn id="5" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.opacity</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst><p:tav tm="0"><p:val><p:strVal val="1"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="0"/></p:val></p:tav></p:tavLst></p:anim><p:set><p:cBhvr><p:cTn id="6" dur="1" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="hidden"/></p:to></p:set>`;
}

function flyInXml(spid, dur, del, direction) {
  const startPos = { l: "-1000000;0", r: "1000000;0", t: "0;-1000000", b: "0;1000000", tl: "-1000000;-1000000", tr: "1000000;-1000000", bl: "-1000000;1000000", br: "1000000;1000000" };
  const start = startPos[direction] || startPos["b"];
  return `<p:set><p:cBhvr><p:cTn id="5" dur="1" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:anim><p:cBhvr><p:cTn id="6" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>ppt_x</p:attrName><p:attrName>ppt_y</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst><p:tav tm="0"><p:val><p:strVal val="${start}"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="0;0"/></p:val></p:tav></p:tavLst></p:anim>`;
}

function flyOutXml(spid, dur, del, direction) {
  const endPos = { l: "-1000000;0", r: "1000000;0", t: "0;-1000000", b: "0;1000000" };
  const end = endPos[direction] || endPos["l"];
  return `<p:anim><p:cBhvr><p:cTn id="5" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>ppt_x</p:attrName><p:attrName>ppt_y</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst><p:tav tm="0"><p:val><p:strVal val="0;0"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="${end}"/></p:val></p:tav></p:tavLst></p:anim><p:set><p:cBhvr><p:cTn id="6" dur="1" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="hidden"/></p:to></p:set>`;
}

function wipeInXml(spid, dur, del, direction) {
  const dirMap = { l: "l", r: "r", t: "t", b: "b", left: "l", right: "r", top: "t", bottom: "b" };
  const d = dirMap[direction] || "b";
  return `<p:set><p:cBhvr><p:cTn id="5" dur="1" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="wipe(${d})"><p:cBhvr><p:cTn id="6" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr></p:animEffect>`;
}

function zoomInXml(spid, dur, del) {
  return `<p:set><p:cBhvr><p:cTn id="5" dur="1" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="zoom()"><p:cBhvr><p:cTn id="6" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr></p:animEffect>`;
}

function floatInXml(spid, dur, del, direction) {
  const dirMap = { l: "l", r: "r", t: "t", b: "b" };
  const d = dirMap[direction] || "b";
  return `<p:set><p:cBhvr><p:cTn id="5" dur="1" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="float(${d})"><p:cBhvr><p:cTn id="6" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr></p:animEffect>`;
}

function floatOutXml(spid, dur, del, direction) {
  const dirMap = { l: "l", r: "r", t: "t", b: "b" };
  const d = dirMap[direction] || "b";
  return `<p:animEffect transition="out" filter="float(${d})"><p:cBhvr><p:cTn id="5" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr></p:animEffect>`;
}

function splitInXml(spid, dur, del, direction) {
  const d = direction === "horiz" || direction === "h" ? "horiz" : "vert";
  return `<p:set><p:cBhvr><p:cTn id="5" dur="1" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="split(${d})"><p:cBhvr><p:cTn id="6" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr></p:animEffect>`;
}

function blindsInXml(spid, dur, del, direction) {
  const d = direction === "horiz" || direction === "h" ? "horiz" : "vert";
  return `<p:set><p:cBhvr><p:cTn id="5" dur="1" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="blinds(${d})"><p:cBhvr><p:cTn id="6" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr></p:animEffect>`;
}

function boxInXml(spid, dur, del, direction) {
  const dirMap = { l: "l", r: "r", t: "t", b: "b" };
  const d = dirMap[direction] || "b";
  return `<p:set><p:cBhvr><p:cTn id="5" dur="1" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="box(${d})"><p:cBhvr><p:cTn id="6" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr></p:animEffect>`;
}

function dissolveInXml(spid, dur, del) {
  return `<p:set><p:cBhvr><p:cTn id="5" dur="1" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="dissolve()"><p:cBhvr><p:cTn id="6" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr></p:animEffect>`;
}

function expandInXml(spid, dur, del) {
  return `<p:set><p:cBhvr><p:cTn id="5" dur="1" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="expand()"><p:cBhvr><p:cTn id="6" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr></p:animEffect>`;
}

function growAndTurnXml(spid, dur, del) {
  return `<p:set><p:cBhvr><p:cTn id="5" dur="1" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="grow-turn()"><p:cBhvr><p:cTn id="6" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr></p:animEffect>`;
}

function swivelXml(spid, dur, del) {
  return `<p:set><p:cBhvr><p:cTn id="5" dur="1" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="swivel()"><p:cBhvr><p:cTn id="6" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr></p:animEffect>`;
}

function pulseXml(spid, dur, del) {
  return `<p:animScale><p:cBhvr><p:cTn id="5" dur="${dur / 2}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr><p:to x="110000" y="110000"/></p:animScale><p:animScale><p:cBhvr><p:cTn id="6" dur="${dur / 2}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr><p:to x="100000" y="100000"/></p:animScale>`;
}

function spinXml(spid, dur, del, degrees) {
  const deg = degrees || 360;
  return `<p:animRot><p:cBhvr><p:cTn id="5" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr><p:by><p:rot val="${deg * 60000}"/></p:by></p:animRot>`;
}

function scaleXml(spid, dur, del, pct) {
  return `<p:animScale><p:cBhvr><p:cTn id="5" dur="${dur}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr><p:to x="${pct}" y="${pct}"/></p:animScale>`;
}

function teeterXml(spid, dur, del) {
  return `<p:animRot><p:cBhvr><p:cTn id="5" dur="${dur / 4}" fill="hold"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr><p:by><p:rot val="1800000"/></p:by></p:animRot><p:animRot><p:cBhvr><p:cTn id="6" dur="${dur / 2}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr><p:by><p:rot val="-3600000"/></p:by></p:animRot><p:animRot><p:cBhvr><p:cTn id="7" dur="${dur / 4}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr><p:by><p:rot val="1800000"/></p:by></p:animRot>`;
}

function blinkXml(spid, dur, del) {
  return `<p:anim><p:cBhvr><p:cTn id="5" dur="${dur}" fill="hold" repeatCount="3"><p:stCondLst><p:cond delay="${del}"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst><p:tav tm="0"><p:val><p:strVal val="visible"/></p:val></p:tav><p:tav tm="50000"><p:val><p:strVal val="hidden"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="visible"/></p:val></p:tav></p:tavLst></p:anim>`;
}

// ─── Build full timing XML for a set of animations ───────────────────────────

function buildTimingXml(animations) {
  if (!animations || animations.length === 0) return "";

  let nextId = 5;
  const effects = [];

  for (const anim of animations) {
    const effectXml = buildEffectXml(
      anim.effect || "fadeIn",
      anim.targetSpid,
      anim.duration || 1000,
      anim.delay || 0,
      anim.direction
    );
    // Reassign IDs to be unique
    const reassignId = (xml) => {
      const id1 = nextId++;
      const id2 = nextId++;
      return xml.replace(/id="5"/, `id="${id1}"`).replace(/id="6"/, `id="${id2}"`);
    };
    effects.push(reassignId(effectXml));
  }

  // Build trigger conditions
  const parItems = effects.map((effectXml, i) => {
    const anim = animations[i];
    const trigger = anim.trigger || "withPrev";
    const delay = anim.delay || 0;

    if (trigger === "afterPrev" && i > 0) {
      return `<p:par><p:cTn id="${nextId++}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="${nextId++}" fill="hold"><p:stCondLst><p:cond delay="${delay}"/></p:stCondLst><p:childTnLst>${effectXml}</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>`;
    }
    return `<p:par><p:cTn id="${nextId++}" fill="hold"><p:stCondLst><p:cond delay="${delay}"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="${nextId++}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>${effectXml}</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>`;
  });

  return `<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>${parItems.join("")}</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>`;
}

// ─── Parse slide XML to find shape IDs ───────────────────────────────────────

function findShapeIds(slideXml) {
  // Find all elements and extract their shape IDs
  // PptxGenJS uses: <p:nvSpPr><p:cNvPr id="X" name="..."></p:cNvPr>
  // Also handles self-closing: <p:cNvPr id="X" name="..." />
  const shapeIds = [];

  // Match <p:cNvPr id="X" ...> (both self-closing and non-self-closing)
  // Only match elements inside nvSpPr, nvPicPr, or nvGraphicFramePr (skip cSld/cSldPr)
  const contexts = [
    /<p:nvSpPr>[\s\S]*?<p:cNvPr[^>]*?id="(\d+)"[^>]*?>/g,
    /<p:nvPicPr>[\s\S]*?<p:cNvPr[^>]*?id="(\d+)"[^>]*?>/g,
    /<p:nvGraphicFramePr>[\s\S]*?<p:cNvPr[^>]*?id="(\d+)"[^>]*?>/g,
  ];

  for (const regex of contexts) {
    let match;
    while ((match = regex.exec(slideXml)) !== null) {
      shapeIds.push(parseInt(match[1], 10));
    }
  }

  // Sort by order of appearance
  return shapeIds;
}

// ─── Main post-processor ─────────────────────────────────────────────────────

async function addAnimations(pptxPath, animConfig, outputPath) {
  const data = fs.readFileSync(pptxPath);
  const zip = await JSZip.loadAsync(data);

  const slideFiles = Object.keys(zip.files)
    .filter(f => f.match(/^ppt\/slides\/slide\d+\.xml$/))
    .sort((a, b) => {
      const numA = parseInt(a.match(/slide(\d+)\.xml/)[1], 10);
      const numB = parseInt(b.match(/slide(\d+)\.xml/)[1], 10);
      return numA - numB;
    });

  for (let i = 0; i < slideFiles.length; i++) {
    const slideFile = slideFiles[i];
    const slideNum = i + 1;
    const slideNumStr = String(slideNum);

    let slideXml = await zip.file(slideFile).async("string");
    const shapeIds = findShapeIds(slideXml);

    // ── Inject slide transition ──
    const transConfig = animConfig.transitions?.[slideNumStr] || animConfig.transitions?.default;
    if (transConfig) {
      const transXml = transitionXml(transConfig);
      // Insert after </p:cSld> if no transition exists yet
      if (!slideXml.includes("<p:transition")) {
        slideXml = slideXml.replace("</p:cSld>", `</p:cSld>${transXml}`);
      } else {
        // Replace existing transition
        slideXml = slideXml.replace(/<p:transition[\s\S]*?<\/p:transition>/, transXml);
      }
    }

    // ── Inject element animations ──
    const slideAnims = animConfig.animations?.[slideNumStr];
    if (slideAnims && slideAnims.length > 0) {
      // Map target indices to shape IDs
      const mappedAnims = slideAnims.map(anim => {
        const targetIdx = typeof anim.target === "number" ? anim.target : 0;
        if (targetIdx >= shapeIds.length) {
          console.warn(`Slide ${slideNum}: target index ${targetIdx} out of range (max ${shapeIds.length - 1}), skipping`);
          return null;
        }
        return { ...anim, targetSpid: shapeIds[targetIdx] };
      }).filter(Boolean);

      if (mappedAnims.length > 0) {
        const timingXml = buildTimingXml(mappedAnims);

        // Remove existing timing if present
        if (slideXml.includes("<p:timing")) {
          slideXml = slideXml.replace(/<p:timing[\s\S]*?<\/p:timing>/, "");
        }

        // Insert before </p:sld>
        slideXml = slideXml.replace("</p:sld>", `${timingXml}</p:sld>`);
      }
    }

    // Write modified XML back
    zip.file(slideFile, slideXml);
  }

  const outPath = outputPath || pptxPath;
  const buffer = await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" });
  fs.writeFileSync(outPath, buffer);
  console.log(`Animations applied: ${outPath}`);
}

// ─── CLI ─────────────────────────────────────────────────────────────────────

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error("Usage: node add_animations.js <pptx-file> <animations.json> [output-file]");
    process.exit(1);
  }

  const pptxPath = args[0];
  const animPath = args[1];
  const outputPath = args[2];

  if (!fs.existsSync(pptxPath)) {
    console.error(`PPTX file not found: ${pptxPath}`);
    process.exit(1);
  }
  if (!fs.existsSync(animPath)) {
    console.error(`Animations config not found: ${animPath}`);
    process.exit(1);
  }

  const animConfig = JSON.parse(fs.readFileSync(animPath, "utf8"));
  addAnimations(pptxPath, animConfig, outputPath).catch(err => {
    console.error("Error:", err.message);
    process.exit(1);
  });
}

module.exports = { addAnimations, transitionXml, buildEffectXml };
