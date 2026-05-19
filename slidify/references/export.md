# Export Reference

## Quick Commands

```bash
# PPTX -> PDF
bash scripts/export.sh output.pptx pdf

# PPTX -> PPT (legacy, rare)
bash scripts/export.sh output.pptx ppt

# PPTX -> both PDF and PPT
bash scripts/export.sh output.pptx all

# PPTX -> slide images (for QA / preview)
bash scripts/export.sh output.pptx images
```

---

## Under the Hood — LibreOffice

Export uses LibreOffice in headless mode:

```bash
# PDF
soffice --headless --convert-to pdf output.pptx

# PPT (legacy binary format)
soffice --headless --convert-to ppt output.pptx

# Custom output dir
soffice --headless --convert-to pdf --outdir ./exports output.pptx
```

LibreOffice must be installed: `sudo apt install libreoffice` or `brew install --cask libreoffice`.

---

## PDF Quality Options

```bash
# High-quality PDF (300 DPI equivalent, larger file)
soffice --headless --convert-to pdf:writer_pdf_Export output.pptx

# Compressed PDF (smaller file)
soffice --headless --convert-to "pdf:writer_pdf_Export:ReduceImageResolution=true" output.pptx
```

---

## Slide Image Export (for QA)

```bash
# Convert to PDF first, then rasterize to JPG
soffice --headless --convert-to pdf output.pptx

rm -f slide-*.jpg
pdftoppm -jpeg -r 150 output.pdf slide
ls -1 "$PWD"/slide-*.jpg   # view each image
```

`-r 150` = 150 DPI, good for QA. Use `-r 300` for print-quality images.

---

## Output Naming Convention

```
output.pptx        -> main editable file
output.pdf         -> for submission / sharing
output-slides/     -> slide-001.jpg, slide-002.jpg, ...
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `soffice: command not found` | Install LibreOffice |
| PDF missing fonts | Use system fonts only in pptxgenjs |
| Images missing in PDF | Use absolute paths or base64 data |
| PDF looks different from PPTX | LibreOffice renders slightly differently |
| `pdftoppm: command not found` | `sudo apt install poppler-utils` |

---

## Batch Export

```bash
for f in *.pptx; do
  soffice --headless --convert-to pdf "$f"
done
```
