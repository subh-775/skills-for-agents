# Animations Reference

PptxGenJS has **no native animation or transition support**. Slidify solves this
with a post-processing step: after PptxGenJS generates the `.pptx` (a ZIP file),
`scripts/add_animations.js` uses JSZip to inject OOXML animation/transition XML
directly into the slide XML files.

---

## How It Works

```
slides.json  →  gen_pptx.js  →  output.pptx (static)
                                        ↓
                              add_animations.js (post-process)
                                        ↓
                              output.pptx (with animations)
```

The post-processor:
1. Opens the `.pptx` ZIP
2. Reads each `ppt/slides/slideN.xml`
3. Injects `<p:transition>` (slide transition) and/or `<p:timing>` (element animations)
4. Saves the modified ZIP

---

## Slide Transitions

Transitions play **between slides** — the visual effect when moving from one slide to the next.

### Supported Transition Types

| Type | OOXML Tag | Directions | Notes |
|------|-----------|------------|-------|
| `fade` | `<p:fade/>` | — | Smooth opacity crossfade |
| `push` | `<p:push dir="..."/>` | `l`, `r`, `t`, `b` | New slide pushes old out |
| `cover` | `<p:cover dir="..."/>` | `l`, `r`, `t`, `b` | New slide covers old |
| `uncover` | `<p:uncover dir="..."/>` | `l`, `r`, `t`, `b` | Old slide uncovers new |
| `wipe` | `<p:wipe dir="..."/>` | `l`, `r`, `t`, `b` | Linear wipe reveal |
| `split` | `<p:split orient="..." dir="..."/>` | `horiz`/`vert`, `in`/`out` | Split reveal |
| `zoom` | `<p:zoom/>` | — | Zoom in/out effect |
| `cut` | `<p:cut/>` | — | Instant cut (no animation) |
| `dissolve` | `<p:dissolve/>` | — | Pixel dissolve |
| `blinds` | `<p:blinds orient="..."/>` | `horiz`/`vert` | Venetian blind reveal |
| `checker` | `<p:checker dir="..."/>` | `l`, `r` | Checkerboard pattern |
| `circle` | `<p:circle/>` | — | Circle iris reveal |
| `diamond` | `<p:diamond/>` | — | Diamond iris reveal |
| `newsflash` | `<p:newsflash/>` | — | Newspaper-style reveal |
| `plus` | `<p:plus/>` | — | Plus-shaped iris |
| `wedge` | `<p:wedge/>` | — | Wedge/pie reveal |
| `wheel` | `<p:wheel spokes="..."/>` | — | Clock wipe (1-8 spokes) |
| `random` | `<p:random/>` | — | Random transition each time |
| `flyThrough` | `<p:flyThrough dir="..."/>` | `l`, `r` | Fly through effect |
| `gallery` | `<p:gallery/>` | — | Gallery-style slide |
| `convey` | `<p:convey/>` | — | Conveyor belt effect |
| `pan` | `<p:pan dir="..."/>` | `l`, `r`, `t`, `b` | Pan/scroll effect |
| `glitter` | `<p:glitter dir="..."/>` | `l`, `r`, `t`, `b` | Glitter/sparkle |
| `vortex` | `<p:vortex/>` | — | Vortex spin |
| `switch` | `<p:switch dir="..."/>` | `l`, `r` | Card flip switch |
| `flip` | `<p:flip dir="..."/>` | `l`, `r` | Flip transition |
| `fall` | `<p:fall/>` | — | Gravity fall |
| `fracture` | `<p:fracture/>` | — | Shatter/fracture |
| `crush` | `<p:crush/>` | — | Crush effect |
| `peelOff` | `<p:peelOff/>` | — | Peel off page |

### Transition Speed

```xml
<p:transition spd="slow|med|fast" advClick="1" advTm="0">
  <p:fade/>
</p:transition>
```

- `spd`: `"slow"` (~1.5s), `"med"` (~0.75s), `"fast"` (~0.35s)
- `advClick`: `1` = advance on click (default)
- `advTm`: milliseconds for auto-advance (0 = manual)

---

## Element Animations

Animations play **on individual elements** (text, shapes, images) when a slide appears.

### Animation Categories

**Entrance** — element appears with effect:

| Name | Preset ID | Class | Subtype |
|------|-----------|-------|---------|
| `fadeIn` | `10` | `entr` | — |
| `flyIn` | `2` | `entr` | `l`, `r`, `t`, `b`, `tl`, `tr`, `bl`, `br` |
| `wipe` | `22` | `entr` | `l`, `r`, `t`, `b` |
| `zoom` | `53` | `entr` | — |
| `floatIn` | `28` | `entr` | `l`, `r`, `t`, `b` |
| `split` | `49` | `entr` | `horiz`, `vert` |
| `blinds` | `3` | `entr` | `horiz`, `vert` |
| `box` | `4` | `entr` | `l`, `r`, `t`, `b` |
| `checkerboard` | `5` | `entr` | `horiz`, `vert` |
| `circle` | `6` | `entr` | — |
| `diamond` | `7` | `entr` | — |
| `dissolve` | `8` | `entr` | — |
| `peek` | `37` | `entr` | `l`, `r`, `t`, `b` |
| `plus` | `38` | `entr` | — |
| `randomBars` | `39` | `entr` | `horiz`, `vert` |
| `wedge` | `51` | `entr` | — |
| `wheel` | `52` | `entr` | spokes: 1-8 |
| `expand` | `11` | `entr` | — |
| `swivel` | `47` | `entr` | — |
| `growAndTurn` | `13` | `entr` | — |

**Exit** — element disappears with effect:

| Name | Preset ID | Class | Subtype |
|------|-----------|-------|---------|
| `fadeOut` | `44` | `exit` | — |
| `flyOut` | `43` | `exit` | `l`, `r`, `t`, `b` |
| `wipe` | `55` | `exit` | `l`, `r`, `t`, `b` |
| `zoom` | `57` | `exit` | — |
| `floatOut` | `54` | `exit` | `l`, `r`, `t`, `b` |
| `shrinkAndTurn` | `60` | `exit` | — |
| `collapse` | `42` | `exit` | — |

**Emphasis** — element changes while visible:

| Name | Preset ID | Class | Subtype |
|------|-----------|-------|---------|
| `pulse` | `28` | `emph` | — |
| `spin` | `38` | `emph` | degrees |
| `grow` | `24` | `emph` | percentage |
| `shrink` | `25` | `emph` | percentage |
| `teeter` | `42` | `emph` | — |
| `blink` | `5` | `emph` | — |
| `colorWave` | `8` | `emph` | color |
| `desaturate` | `9` | `emph` | — |
| `darken` | `10` | `emph` | — |
| `lighten` | `11` | `emph` | — |
| `transparency` | `43` | `emph` | percentage |

### Animation Timing Properties

| Property | Default | Description |
|----------|---------|-------------|
| `duration` | `1000` | Animation duration in ms |
| `delay` | `0` | Delay before animation starts (ms) |
| `trigger` | `onClick` | `onClick`, `withPrev`, `afterPrev`, `onNext` |
| `repeat` | `0` | Number of times to repeat (0 = once) |
| `ease` | `linear` | Easing: `linear`, `easeIn`, `easeOut`, `easeInOut` |
| `autoReverse` | `false` | Play in reverse after completing |

### Animation Sequencing

Animations are sequenced via the `trigger` property:

```json
{
  "animate": [
    { "target": "title", "effect": "fadeIn", "trigger": "withPrev", "duration": 800 },
    { "target": "body", "effect": "flyIn", "direction": "b", "trigger": "afterPrev", "delay": 200 },
    { "target": "image", "effect": "zoom", "trigger": "afterPrev" }
  ]
}
```

- `withPrev` — plays at the same time as the previous animation
- `afterPrev` — plays after the previous animation finishes
- `onClick` — plays when the presenter clicks

---

## OOXML Structure

### Slide Transition XML

Injected as a child of `<p:sld>`, after `<p:cSld>`:

```xml
<p:sld>
  <p:cSld>...</p:cSld>
  <p:transition spd="med" advClick="1" advTm="0">
    <p:fade/>
  </p:transition>
</p:sld>
```

### Element Animation XML (Entrance)

```xml
<p:timing>
  <p:tnLst>
    <p:par>
      <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
        <p:childTnLst>
          <p:seq concurrent="1" nextAc="seek">
            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
              <p:childTnLst>
                <p:par>
                  <p:cTn id="3" fill="hold">
                    <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                    <p:childTnLst>
                      <p:par>
                        <p:cTn id="4" fill="hold">
                          <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                          <p:childTnLst>
                            <!-- Effect here -->
                          </p:childTnLst>
                        </p:cTn>
                      </p:par>
                    </p:childTnLst>
                  </p:cTn>
                </p:par>
              </p:childTnLst>
            </p:cTn>
          </p:seq>
        </p:childTnLst>
      </p:cTn>
    </p:par>
  </p:tnLst>
</p:timing>
```

### Fade-In Entrance Example

```xml
<p:set>
  <p:cBhvr>
    <p:cTn id="5" dur="1" fill="hold">
      <p:stCondLst><p:cond delay="0"/></p:stCondLst>
    </p:cTn>
    <p:tgtEl><p:spTgt spid="SHAPE_ID"/></p:tgtEl>
    <p:attrNameLst>
      <p:attrName>style.visibility</p:attrName>
    </p:attrNameLst>
  </p:cBhvr>
  <p:to><p:strVal val="visible"/></p:to>
</p:set>
<p:anim>
  <p:cBhvr>
    <p:cTn id="6" dur="DURATION_MS" fill="hold"/>
    <p:tgtEl><p:spTgt spid="SHAPE_ID"/></p:tgtEl>
    <p:attrNameLst>
      <p:attrName>style.opacity</p:attrName>
    </p:attrNameLst>
  </p:cBhvr>
  <p:tavLst>
    <p:tav tm="0"><p:val><p:strVal val="0"/></p:val></p:tav>
    <p:tav tm="100000"><p:val><p:strVal val="1"/></p:val></p:tav>
  </p:tavLst>
</p:anim>
```

### Fly-In Entrance Example

```xml
<p:set>
  <p:cBhvr>
    <p:cTn id="5" dur="1" fill="hold">
      <p:stCondLst><p:cond delay="0"/></p:stCondLst>
    </p:cTn>
    <p:tgtEl><p:spTgt spid="SHAPE_ID"/></p:tgtEl>
    <p:attrNameLst>
      <p:attrName>style.visibility</p:attrName>
    </p:attrNameLst>
  </p:cBhvr>
  <p:to><p:strVal val="visible"/></p:to>
</p:set>
<p:anim>
  <p:cBhvr>
    <p:cTn id="6" dur="DURATION_MS" fill="hold"/>
    <p:tgtEl><p:spTgt spid="SHAPE_ID"/></p:tgtEl>
    <p:attrNameLst>
      <p:attrName>ppt_x</p:attrName>
      <p:attrName>ppt_y</p:attrName>
    </p:attrNameLst>
  </p:cBhvr>
  <p:tavLst>
    <p:tav tm="0"><p:val><p:strVal val="START_X;START_Y"/></p:val></p:tav>
    <p:tav tm="100000"><p:val><p:strVal val="END_X;END_Y"/></p:val></p:tav>
  </p:tavLst>
</p:anim>
```

### Preset Animation Effect (Simpler Approach)

PowerPoint uses preset effect IDs. The `<p:presetClass>` approach is simpler:

```xml
<p:animEffect transition="in" filter="fade">
  <p:cBhvr>
    <p:cTn id="5" dur="DURATION_MS" fill="hold"/>
    <p:tgtEl><p:spTgt spid="SHAPE_ID"/></p:tgtEl>
  </p:cBhvr>
</p:animEffect>
```

---

## Targeting Elements by Shape ID

Each element on a slide gets a `spid` (shape ID) in the OOXML. The post-processor
must find these IDs to attach animations. Shape IDs are assigned sequentially in
the slide XML — the first `<p:sp>` gets spid="2", the next gets spid="3", etc.

The post-processor reads the slide XML, counts `<p:sp>` elements to build a
shape index, then uses that index to target animations.

---

## Animation Presets (Quick Reference)

### Presentation Types → Recommended Animations

| Presentation Type | Entrance | Transitions | Emphasis |
|------------------|----------|-------------|----------|
| **Research/Academic** | `fadeIn`, `zoom` | `fade`, `dissolve` | `pulse` (on stats) |
| **Corporate/Business** | `flyIn`, `wipe` | `push`, `cover` | `grow` (on KPIs) |
| **Creative/Portfolio** | `floatIn`, `swivel` | `glitter`, `vortex` | `spin`, `colorWave` |
| **Technical/Engineering** | `wipe`, `box` | `wipe`, `split` | `blink` (on warnings) |
| **Conference Talk** | `fadeIn`, `growAndTurn` | `fade`, `zoom` | `teeter` (on key points) |
| **Teaching/Lecture** | `fadeIn`, `blinds` | `fade`, `dissolve` | `pulse` |
| **Startup Pitch** | `flyIn`, `expand` | `push`, `flyThrough` | `grow`, `colorWave` |
| **Minimalist** | `fadeIn` | `fade` | None |

---

## Gotchas and Limitations

1. **Shape IDs are dynamic** — the post-processor must parse the XML to find them, not assume values
2. **Timing conflicts** — too many simultaneous animations can cause rendering issues
3. **LibreOffice** — may not render all animations when exporting to PDF
4. **Google Slides** — supports a subset; `fade`, `flyIn`, `wipe` work; exotic effects may not
5. **Keynote** — imports most transitions but some animations may differ
6. **Mobile viewers** — many mobile PPTX viewers ignore animations entirely
7. **Auto-advance** — if `advTm` is set on transitions, the presentation auto-advances
