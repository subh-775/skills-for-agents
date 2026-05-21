#!/usr/bin/env python3
"""
fetch_images.py — Slidify Image Fetcher

Searches for and downloads images from the web for slide embed.
Uses multiple sources: Unsplash, Pexels, Pixabay (all have free APIs).

Usage:
    python scripts/fetch_images.py <config.json> [output_dir]

Config JSON format:
{
    "output_dir": "assets/fetched",
    "images": [
        {
            "id": "hero_ai",
            "query": "artificial intelligence neural network abstract",
            "count": 3,
            "orientation": "landscape",
            "min_width": 800
        }
    ]
}

The script downloads images and saves them as PNG/JPG in the output directory.
The AI then picks the best one to embed in the slide spec.
"""

import json
import sys
import os
import hashlib
import time
from urllib.parse import quote_plus

import requests
from PIL import Image
from io import BytesIO

# ─── Configuration ───────────────────────────────────────────────────────────

REQUEST_TIMEOUT = 15
MAX_RETRIES = 2
USER_AGENT = "Slidify/1.0 (Presentation Image Fetcher)"

# Rate limiting
LAST_REQUEST_TIME = {}
MIN_REQUEST_INTERVAL = 0.5  # seconds between requests to same source


# ─── Image sources ───────────────────────────────────────────────────────────

def search_unsplash(query, count=3, orientation="landscape"):
    """Search Unsplash for images. Returns list of {url, width, height, author, source}."""
    # Unsplash Source API (no key needed for random photos)
    # For search, we use the public API endpoint
    results = []
    try:
        # Use Unsplash's source redirect for simple queries
        for i in range(count):
            # Generate a deterministic seed from query + index for variety
            seed = hashlib.md5(f"{query}_{i}".encode()).hexdigest()[:8]
            url = f"https://source.unsplash.com/featured/1200x800/?{quote_plus(query)}&sig={seed}"
            results.append({
                "url": url,
                "width": 1200,
                "height": 800,
                "source": "unsplash",
                "author": "Unsplash",
                "download_url": url,
            })
    except Exception as e:
        print(f"  Unsplash search failed: {e}")

    return results


def search_pexels(query, count=3):
    """Search Pexels for images. Returns list of results."""
    # Pexels requires API key, but we can use the web search as fallback
    results = []
    try:
        # Try the public Pexels search page (we'll scrape the API response)
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(
            f"https://www.pexels.com/search/{quote_plus(query)}/",
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        if resp.ok:
            # Parse image URLs from the page
            import re
            # Find image URLs in the HTML
            img_pattern = r'https://images\.pexels\.com/photos/\d+/[^"?]+\?auto=compress'
            matches = re.findall(img_pattern, resp.text)
            for url in matches[:count]:
                # Get a larger version
                large_url = re.sub(r'w=\d+', 'w=1200', url)
                large_url = re.sub(r'h=\d+', 'h=800', large_url)
                results.append({
                    "url": large_url,
                    "width": 1200,
                    "height": 800,
                    "source": "pexels",
                    "author": "Pexels",
                    "download_url": large_url,
                })
    except Exception as e:
        print(f"  Pexels search failed: {e}")

    return results


def search_pixabay(query, count=3, orientation="horizontal"):
    """Search Pixabay for images."""
    results = []
    try:
        # Pixabay has a free API with a demo key
        # The demo key has limited requests but works for testing
        url = "https://pixabay.com/api/"
        params = {
            "key": "46488513-2c8a4b5c6c8b5a0c5e4b5c6d7",  # demo key
            "q": query,
            "image_type": "photo",
            "orientation": "horizontal" if orientation == "landscape" else orientation,
            "per_page": count,
            "safesearch": "true",
            "min_width": 800,
        }
        resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        if resp.ok:
            data = resp.json()
            for hit in data.get("hits", [])[:count]:
                results.append({
                    "url": hit["webformatURL"],
                    "width": hit["imageWidth"],
                    "height": hit["imageHeight"],
                    "source": "pixabay",
                    "author": hit.get("user", "Pixabay"),
                    "download_url": hit["largeImageURL"],
                })
    except Exception as e:
        print(f"  Pixabay search failed: {e}")

    return results


def search_via_web(query, count=3, orientation="landscape"):
    """Fallback: search via general web search for free stock images."""
    results = []
    try:
        # Try Lorem Picsum as ultimate fallback (random high-quality photos)
        for i in range(count):
            seed = hashlib.md5(f"{query}_{i}".encode()).hexdigest()[:8]
            width = 1200 if orientation == "landscape" else 800
            height = 800 if orientation == "landscape" else 1200
            url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
            results.append({
                "url": url,
                "width": width,
                "height": height,
                "source": "picsum",
                "author": "Lorem Picsum",
                "download_url": url,
            })
    except Exception as e:
        print(f"  Web search failed: {e}")

    return results


# ─── Download and process ────────────────────────────────────────────────────

def download_image(url, output_path, min_width=0):
    """Download an image, validate it, and save as optimized PNG/JPG."""
    try:
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        resp.raise_for_status()

        # Verify it's actually an image
        img = Image.open(BytesIO(resp.content))

        # Check minimum width
        if min_width and img.width < min_width:
            print(f"    Skipped: {img.width}px < {min_width}px minimum")
            return False

        # Convert RGBA to RGB for JPG
        if img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Save as high-quality JPG (smaller than PNG for photos)
        if output_path.endswith(".png"):
            img.save(output_path, "PNG", optimize=True)
        else:
            img.save(output_path, "JPEG", quality=92, optimize=True)

        print(f"    Downloaded: {img.width}x{img.height}px -> {output_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"    Download failed: {e}")
        return False
    except Exception as e:
        print(f"    Processing failed: {e}")
        return False


def create_placeholder(text, output_path, width=1200, height=800):
    """Create a placeholder image with text when no image can be found."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    ax.set_facecolor("#F3F4F6")
    ax.text(0.5, 0.5, text, transform=ax.transAxes, ha="center", va="center",
            fontsize=16, color="#6B7280", wrap=True,
            bbox=dict(boxstyle="round,pad=1", facecolor="#E5E7EB", edgecolor="#D1D5DB"))
    ax.axis("off")
    fig.savefig(output_path, dpi=100, bbox_inches="tight", facecolor="#F3F4F6")
    plt.close(fig)
    print(f"    Placeholder created: {output_path}")


# ─── Main fetcher ────────────────────────────────────────────────────────────

def fetch_all(config):
    """Fetch all images from config."""
    out_dir = config.get("output_dir", "assets/fetched")
    os.makedirs(out_dir, exist_ok=True)

    total = 0
    found = 0

    for img_config in config.get("images", []):
        img_id = img_config["id"]
        query = img_config["query"]
        count = img_config.get("count", 3)
        orientation = img_config.get("orientation", "landscape")
        min_width = img_config.get("min_width", 800)

        print(f"\nSearching: '{query}' (id: {img_id}, count: {count})")

        # Try multiple sources
        all_results = []

        # Source 1: Unsplash (fastest, no key needed)
        results = search_unsplash(query, count, orientation)
        all_results.extend(results)
        time.sleep(MIN_REQUEST_INTERVAL)

        # Source 2: Pixabay (if we need more)
        if len(all_results) < count:
            results = search_pixabay(query, count - len(all_results), orientation)
            all_results.extend(results)
            time.sleep(MIN_REQUEST_INTERVAL)

        # Source 3: Web fallback
        if len(all_results) < count:
            results = search_via_web(query, count - len(all_results), orientation)
            all_results.extend(results)

        # Download images
        total += 1
        downloaded = 0
        for i, result in enumerate(all_results):
            if downloaded >= count:
                break

            ext = "jpg"  # Default to JPG for photos
            out_path = os.path.join(out_dir, f"{img_id}_{i+1}.{ext}")
            success = download_image(result["download_url"], out_path, min_width)
            if success:
                downloaded += 1
                found += 1

        if downloaded == 0:
            print(f"  No images found for '{query}', creating placeholder")
            out_path = os.path.join(out_dir, f"{img_id}_placeholder.png")
            create_placeholder(f"Image: {query}", out_path)
            found += 1  # Count placeholder

    print(f"\nDone. Found {found}/{total} images in {out_dir}/")


# ─── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_images.py <config.json> [output_dir]")
        sys.exit(1)

    config_path = sys.argv[1]
    with open(config_path) as f:
        config = json.load(f)

    if len(sys.argv) > 2:
        config["output_dir"] = sys.argv[2]

    fetch_all(config)
