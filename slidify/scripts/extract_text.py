#!/usr/bin/env python3
"""Extract all text from a .pptx file for QA verification."""
import sys
import zipfile
import xml.etree.ElementTree as ET

def extract_text(pptx_path):
    texts = []
    with zipfile.ZipFile(pptx_path) as z:
        slide_files = sorted(f for f in z.namelist() if f.startswith("ppt/slides/slide") and f.endswith(".xml"))
        for sf in slide_files:
            tree = ET.parse(z.open(sf))
            slide_texts = []
            for t in tree.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t"):
                if t.text:
                    slide_texts.append(t.text)
            if slide_texts:
                texts.append({"slide": sf.split("slide")[1].split(".xml")[0], "text": " ".join(slide_texts)})
    return texts

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/extract_text.py <file.pptx>")
        sys.exit(1)
    for item in extract_text(sys.argv[1]):
        print(f"[Slide {item['slide']}] {item['text']}")
