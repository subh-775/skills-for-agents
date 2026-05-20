#!/usr/bin/env bash
# export.sh — Convert .pptx to PDF, PPT, or slide images
# Usage: bash scripts/export.sh <input.pptx> <format>
# Format: pdf | ppt | images | all

set -e

INPUT="${1}"
FORMAT="${2:-pdf}"

if [[ -z "$INPUT" || ! -f "$INPUT" ]]; then
  echo "Usage: bash scripts/export.sh <input.pptx> [pdf|ppt|images|all]"
  exit 1
fi

BASENAME="${INPUT%.pptx}"

export_pdf() {
  echo "Exporting PDF..."
  libreoffice --headless --convert-to pdf "$INPUT"
  echo "Done: ${BASENAME}.pdf"
}

export_ppt() {
  echo "Exporting PPT (legacy)..."
  libreoffice --headless --convert-to ppt "$INPUT"
  echo "Done: ${BASENAME}.ppt"
}

export_images() {
  echo "Exporting slide images..."
  if [[ ! -f "${BASENAME}.pdf" ]]; then
    libreoffice --headless --convert-to pdf "$INPUT"
  fi
  rm -f slide-*.jpg
  pdftoppm -jpeg -r 150 "${BASENAME}.pdf" slide
  COUNT=$(ls slide-*.jpg 2>/dev/null | wc -l)
  echo "Done: ${COUNT} slide images"
}

case "$FORMAT" in
  pdf)    export_pdf   ;;
  ppt)    export_ppt   ;;
  images) export_images ;;
  all)
    export_pdf
    export_ppt
    export_images
    ;;
  *)
    echo "Unknown format: $FORMAT. Use: pdf | ppt | images | all"
    exit 1
    ;;
esac
