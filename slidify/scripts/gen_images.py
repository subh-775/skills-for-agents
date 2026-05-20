#!/usr/bin/env python3
"""
gen_images.py — Slidify Image Generator

Generates charts, diagrams, infographics, and visual assets using matplotlib.
Output: PNG files ready for PPTX embed.

Usage:
    python scripts/gen_images.py <config.json> [output_dir]

Config JSON format:
{
    "output_dir": "assets/generated",
    "images": [
        {
            "id": "perf_chart",
            "type": "bar",
            "title": "Model Performance Comparison",
            "data": {
                "labels": ["Phi-4", "LLaMA", "TokenAdapt"],
                "values": [48.2, 52.1, 24.6],
                "colors": ["#CADCFC", "#CADCFC", "#2563EB"]
            },
            "options": {
                "ylabel": "Perplexity (lower is better)",
                "highlight_best": true,
                "style": "minimal"
            }
        }
    ]
}
"""

import json
import sys
import os
import math

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle as MplCircle
import numpy as np

# ─── Style defaults ──────────────────────────────────────────────────────────

SLIDE_WIDTH = 10   # inches (16:9 aspect)
SLIDE_HEIGHT = 5.625
DPI = 200

STYLE_PRESETS = {
    "minimal": {
        "bg": "#FFFFFF",
        "text": "#1A1A1A",
        "muted": "#6B7280",
        "accent": "#2563EB",
        "grid": "#E5E7EB",
        "font": "sans-serif",
    },
    "dark": {
        "bg": "#1E293B",
        "text": "#F8FAFC",
        "muted": "#94A3B8",
        "accent": "#3B82F6",
        "grid": "#334155",
        "font": "sans-serif",
    },
    "research": {
        "bg": "#FFFFFF",
        "text": "#1E3A5F",
        "muted": "#6B7280",
        "accent": "#C8A951",
        "grid": "#E5E7EB",
        "font": "serif",
    },
    "corporate": {
        "bg": "#FFFFFF",
        "text": "#111827",
        "muted": "#9CA3AF",
        "accent": "#1E40AF",
        "grid": "#F3F4F6",
        "font": "sans-serif",
    },
    "vibrant": {
        "bg": "#FFFFFF",
        "text": "#1A1A1A",
        "muted": "#6B7280",
        "accent": "#EC4899",
        "grid": "#F3F4F6",
        "font": "sans-serif",
    },
}


def get_style(options):
    """Merge preset with overrides."""
    preset = options.get("style", "minimal")
    s = STYLE_PRESETS.get(preset, STYLE_PRESETS["minimal"]).copy()
    for k in ["bg", "text", "muted", "accent", "grid"]:
        if k in options:
            s[k] = options[k]
    return s


def apply_style(fig, ax, s):
    """Apply style to figure and axes."""
    fig.patch.set_facecolor(s["bg"])
    ax.set_facecolor(s["bg"])
    ax.tick_params(colors=s["text"], labelsize=10)
    ax.xaxis.label.set_color(s["text"])
    ax.yaxis.label.set_color(s["text"])
    ax.title.set_color(s["text"])
    for spine in ax.spines.values():
        spine.set_color(s["grid"])


def save(fig, path):
    """Save figure as PNG."""
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor=fig.get_facecolor(),
                pad_inches=0.3, transparent=False)
    plt.close(fig)
    print(f"  Generated: {path}")


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


# ─── Chart generators ────────────────────────────────────────────────────────

def gen_bar(config, out_path):
    """Vertical or horizontal bar chart."""
    data = config["data"]
    options = config.get("options", {})
    s = get_style(options)
    horizontal = options.get("horizontal", False)

    labels = data["labels"]
    values = data["values"]
    colors = data.get("colors", [s["accent"]] * len(values))

    fig, ax = plt.subplots(figsize=(8, 5))
    apply_style(fig, ax, s)

    x = np.arange(len(labels))
    if horizontal:
        bars = ax.barh(x, values, color=colors, height=0.6, edgecolor="none")
        ax.set_yticks(x)
        ax.set_yticklabels(labels, fontsize=11)
        ax.set_xlabel(options.get("xlabel", ""), fontsize=11)
        ax.invert_yaxis()
        for bar, val in zip(bars, values):
            ax.text(bar.get_width() + max(values) * 0.02, bar.get_y() + bar.get_height()/2,
                    f"{val:,.1f}" if isinstance(val, float) else f"{val:,}",
                    va="center", fontsize=10, color=s["text"])
    else:
        bars = ax.bar(x, values, color=colors, width=0.6, edgecolor="none")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=11, rotation=options.get("rotation", 0))
        ax.set_ylabel(options.get("ylabel", ""), fontsize=11)
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values) * 0.02,
                    f"{val:,.1f}" if isinstance(val, float) else f"{val:,}",
                    ha="center", fontsize=10, color=s["text"])

    if options.get("highlight_best"):
        best_idx = min(range(len(values)), key=lambda i: values[i]) if options.get("lower_is_better") else max(range(len(values)), key=lambda i: values[i])
        bars[best_idx].set_edgecolor(s["accent"])
        bars[best_idx].set_linewidth(3)

    if options.get("title"):
        ax.set_title(options["title"], fontsize=14, fontweight="bold", pad=15)

    ax.grid(axis="x" if horizontal else "y", color=s["grid"], alpha=0.5, linewidth=0.5)
    ax.set_axisbelow(True)
    if not horizontal:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    save(fig, out_path)


def gen_grouped_bar(config, out_path):
    """Grouped bar chart for multi-series comparison."""
    data = config["data"]
    options = config.get("options", {})
    s = get_style(options)

    labels = data["labels"]
    series = data["series"]
    n_series = len(series)
    x = np.arange(len(labels))
    width = 0.8 / n_series

    fig, ax = plt.subplots(figsize=(10, 5.5))
    apply_style(fig, ax, s)

    for i, ser in enumerate(series):
        offset = (i - n_series/2 + 0.5) * width
        color = ser.get("color", s["accent"] if i == 0 else s["muted"])
        bars = ax.bar(x + offset, ser["values"], width, label=ser["name"], color=color, edgecolor="none")
        for bar, val in zip(bars, ser["values"]):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(max(ser["values"]) for ser in series) * 0.02,
                    f"{val:,.1f}" if isinstance(val, float) else f"{val:,}",
                    ha="center", fontsize=9, color=s["text"])

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylabel(options.get("ylabel", ""), fontsize=11)
    if options.get("title"):
        ax.set_title(options["title"], fontsize=14, fontweight="bold", pad=15)
    ax.legend(frameon=False, fontsize=10)
    ax.grid(axis="y", color=s["grid"], alpha=0.5, linewidth=0.5)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    save(fig, out_path)


def gen_line(config, out_path):
    """Line chart for trends over time."""
    data = config["data"]
    options = config.get("options", {})
    s = get_style(options)

    labels = data["labels"]
    series = data["series"]

    fig, ax = plt.subplots(figsize=(9, 5))
    apply_style(fig, ax, s)

    for i, ser in enumerate(series):
        color = ser.get("color", s["accent"] if i == 0 else s["muted"])
        marker = ser.get("marker", "o" if i == 0 else "s")
        ax.plot(labels, ser["values"], color=color, marker=marker, markersize=6,
                linewidth=2.5, label=ser["name"])
        # Annotate last point
        ax.annotate(f"{ser['values'][-1]:,.1f}" if isinstance(ser['values'][-1], float) else f"{ser['values'][-1]:,}",
                    xy=(len(labels)-1, ser['values'][-1]),
                    xytext=(10, 10), textcoords="offset points",
                    fontsize=10, color=color, fontweight="bold")

    ax.set_ylabel(options.get("ylabel", ""), fontsize=11)
    if options.get("title"):
        ax.set_title(options["title"], fontsize=14, fontweight="bold", pad=15)
    if len(series) > 1:
        ax.legend(frameon=False, fontsize=10)
    ax.grid(axis="y", color=s["grid"], alpha=0.5, linewidth=0.5)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.xticks(rotation=options.get("rotation", 0))

    save(fig, out_path)


def gen_pie(config, out_path):
    """Pie or donut chart."""
    data = config["data"]
    options = config.get("options", {})
    s = get_style(options)
    donut = options.get("donut", False)

    labels = data["labels"]
    values = data["values"]
    colors = data.get("colors", [plt.cm.get_cmap("Set2")(i / len(values)) for i in range(len(values))])

    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor(s["bg"])

    result = ax.pie(
        values, labels=labels, colors=colors, autopct="%1.0f%%",
        startangle=90, pctdistance=0.75 if donut else 0.6,
        wedgeprops=dict(width=0.4) if donut else dict(),
        textprops=dict(color=s["text"], fontsize=11)
    )
    autotexts = result[2] if len(result) > 2 else []
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight("bold")

    if donut:
        ax.text(0, 0, options.get("center_label", ""), ha="center", va="center",
                fontsize=16, fontweight="bold", color=s["text"])

    if options.get("title"):
        ax.set_title(options["title"], fontsize=14, fontweight="bold", color=s["text"], pad=15)

    save(fig, out_path)


def gen_scatter(config, out_path):
    """Scatter plot."""
    data = config["data"]
    options = config.get("options", {})
    s = get_style(options)

    fig, ax = plt.subplots(figsize=(8, 5.5))
    apply_style(fig, ax, s)

    series_list = data.get("series", [{"name": "Data", "x": data["x"], "y": data["y"]}])
    for i, ser in enumerate(series_list):
        color = ser.get("color", s["accent"] if i == 0 else s["muted"])
        ax.scatter(ser["x"], ser["y"], c=color, s=80, alpha=0.8, edgecolors="white", linewidth=0.5, label=ser.get("name"))
        if options.get("label_points") and "labels" in ser:
            for xi, yi, label in zip(ser["x"], ser["y"], ser["labels"]):
                ax.annotate(label, (xi, yi), xytext=(5, 5), textcoords="offset points", fontsize=9, color=s["text"])

    ax.set_xlabel(options.get("xlabel", ""), fontsize=11)
    ax.set_ylabel(options.get("ylabel", ""), fontsize=11)
    if options.get("title"):
        ax.set_title(options["title"], fontsize=14, fontweight="bold", pad=15)
    if len(series_list) > 1:
        ax.legend(frameon=False, fontsize=10)
    ax.grid(color=s["grid"], alpha=0.5, linewidth=0.5)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    save(fig, out_path)


def gen_heatmap(config, out_path):
    """Heatmap for correlation matrices or confusion matrices."""
    data = config["data"]
    options = config.get("options", {})
    s = get_style(options)

    matrix = np.array(data["matrix"])
    row_labels = data.get("row_labels", [str(i) for i in range(matrix.shape[0])])
    col_labels = data.get("col_labels", [str(i) for i in range(matrix.shape[1])])

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(s["bg"])

    cmap = options.get("colormap", "YlOrRd")
    im = ax.imshow(matrix, cmap=cmap, aspect="auto")

    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticklabels(col_labels, fontsize=10)
    ax.set_yticklabels(row_labels, fontsize=10)

    # Annotate cells
    val_fmt = options.get("value_format", ".1f")
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            val = matrix[i, j]
            color = "white" if val > (matrix.max() + matrix.min()) / 2 else s["text"]
            ax.text(j, i, format(val, val_fmt), ha="center", va="center", fontsize=10, color=color)

    if options.get("title"):
        ax.set_title(options["title"], fontsize=14, fontweight="bold", color=s["text"], pad=15)

    fig.colorbar(im, ax=ax, shrink=0.8)
    save(fig, out_path)


def gen_comparison(config, out_path):
    """Side-by-side comparison visual (before/after or A vs B)."""
    data = config["data"]
    options = config.get("options", {})
    s = get_style(options)

    items = data["items"]  # [{label, value, color}]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    fig.patch.set_facecolor(s["bg"])
    ax.set_facecolor(s["bg"])
    ax.axis("off")

    n = len(items)
    col_width = 0.8 / n

    for i, item in enumerate(items):
        x_center = 0.1 + (i + 0.5) * col_width
        color = item.get("color", s["accent"] if i == 0 else s["muted"])

        # Big value
        ax.text(x_center, 0.65, str(item["value"]), transform=ax.transAxes,
                ha="center", va="center", fontsize=36, fontweight="bold", color=color)
        # Label
        ax.text(x_center, 0.35, item["label"], transform=ax.transAxes,
                ha="center", va="center", fontsize=14, color=s["text"])
        # Sub-label if present
        if "sub" in item:
            ax.text(x_center, 0.22, item["sub"], transform=ax.transAxes,
                    ha="center", va="center", fontsize=10, color=s["muted"])

        # Separator
        if i < n - 1:
            ax.axvline(x=0.1 + (i + 1) * col_width, ymin=0.2, ymax=0.8,
                       color=s["grid"], linewidth=1, transform=ax.transAxes)

    if options.get("title"):
        ax.set_title(options["title"], fontsize=14, fontweight="bold", color=s["text"], pad=15, transform=ax.transAxes)

    save(fig, out_path)


def gen_flowchart(config, out_path):
    """Simple flowchart / process diagram."""
    data = config["data"]
    options = config.get("options", {})
    s = get_style(options)

    steps = data["steps"]  # [{id, label, sub?}]
    connections = data.get("connections", [])  # [{from, to}]

    n = len(steps)
    fig, ax = plt.subplots(figsize=(max(10, n * 2.2), 4))
    fig.patch.set_facecolor(s["bg"])
    ax.set_facecolor(s["bg"])
    ax.axis("off")
    ax.set_xlim(-0.5, n * 2.5)
    ax.set_ylim(-1.5, 2.5)

    positions = {}
    for i, step in enumerate(steps):
        x = i * 2.5
        y = 0.5
        positions[step["id"]] = (x, y)

        color = step.get("color", s["accent"] if i == 0 or i == n-1 else s["bg"])
        text_color = "#FFFFFF" if color == s["accent"] else s["text"]
        edge_color = s["accent"] if color != s["accent"] else "none"

        box = FancyBboxPatch((x - 0.9, y - 0.5), 1.8, 1.0,
                             boxstyle="round,pad=0.1", facecolor=color,
                             edgecolor=edge_color, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y + 0.1, step["label"], ha="center", va="center",
                fontsize=11, fontweight="bold", color=text_color)
        if "sub" in step:
            ax.text(x, y - 0.25, step["sub"], ha="center", va="center",
                    fontsize=8, color=text_color if text_color == "#FFFFFF" else s["muted"])

        # Arrow to next
        if i < n - 1:
            ax.annotate("", xy=(x + 1.3, y), xytext=(x + 0.9, y),
                        arrowprops=dict(arrowstyle="->", color=s["muted"], lw=2))

    # Custom connections
    for conn in connections:
        fx, fy = positions[conn["from"]]
        tx, ty = positions[conn["to"]]
        ax.annotate("", xy=(tx - 0.9, ty), xytext=(fx + 0.9, fy),
                    arrowprops=dict(arrowstyle="->", color=s["accent"], lw=1.5,
                                    connectionstyle="arc3,rad=0.3"))

    if options.get("title"):
        ax.set_title(options["title"], fontsize=14, fontweight="bold", color=s["text"], pad=15)

    save(fig, out_path)


def gen_timeline(config, out_path):
    """Visual timeline."""
    data = config["data"]
    options = config.get("options", {})
    s = get_style(options)

    events = data["events"]  # [{date, label, icon?}]

    fig, ax = plt.subplots(figsize=(10, 4.5))
    fig.patch.set_facecolor(s["bg"])
    ax.set_facecolor(s["bg"])
    ax.axis("off")
    ax.set_xlim(-0.5, len(events) * 2 + 0.5)
    ax.set_ylim(-2, 2)

    # Main line
    ax.plot([0, len(events) * 2 - 2], [0, 0], color=s["grid"], linewidth=3, zorder=1)

    for i, event in enumerate(events):
        x = i * 2
        # Dot on timeline
        ax.plot(x, 0, "o", markersize=14, color=s["accent"], zorder=2)
        ax.plot(x, 0, "o", markersize=8, color=s["bg"], zorder=3)

        # Alternate above/below
        y_text = 1.2 if i % 2 == 0 else -1.2
        va = "bottom" if i % 2 == 0 else "top"

        # Vertical connector
        ax.plot([x, x], [0, y_text * 0.6], color=s["grid"], linewidth=1, zorder=1)

        # Date
        ax.text(x, y_text, event["date"], ha="center", va=va,
                fontsize=10, fontweight="bold", color=s["accent"])
        # Label
        offset = 0.35 if i % 2 == 0 else -0.35
        ax.text(x, y_text + offset, event["label"], ha="center", va=va,
                fontsize=9, color=s["text"], wrap=True,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=s["bg"], edgecolor=s["grid"], linewidth=0.5))

    if options.get("title"):
        ax.set_title(options["title"], fontsize=14, fontweight="bold", color=s["text"], pad=15)

    save(fig, out_path)


def gen_stat_callout(config, out_path):
    """Big number stat callout cards."""
    data = config["data"]
    options = config.get("options", {})
    s = get_style(options)

    stats = data["stats"]  # [{value, label, icon?, color?}]

    n = len(stats)
    fig, axes = plt.subplots(1, n, figsize=(n * 2.5, 4))
    fig.patch.set_facecolor(s["bg"])
    if n == 1:
        axes = [axes]

    for i, (ax, stat) in enumerate(zip(axes, stats)):
        ax.set_facecolor(s["bg"])
        ax.axis("off")

        color = stat.get("color", s["accent"])
        # Card background
        box = FancyBboxPatch((0.05, 0.05), 0.9, 0.9, boxstyle="round,pad=0.05",
                             facecolor=s["bg"], edgecolor=s["grid"], linewidth=1.5,
                             transform=ax.transAxes)
        ax.add_patch(box)

        # Big value
        ax.text(0.5, 0.6, str(stat["value"]), transform=ax.transAxes,
                ha="center", va="center", fontsize=32, fontweight="bold", color=color)
        # Label
        ax.text(0.5, 0.28, stat["label"], transform=ax.transAxes,
                ha="center", va="center", fontsize=11, color=s["text"])

    fig.suptitle(options.get("title", ""), fontsize=14, fontweight="bold", color=s["text"], y=0.95)

    save(fig, out_path)


def gen_venn(config, out_path):
    """Venn diagram (2-3 circles)."""
    data = config["data"]
    options = config.get("options", {})
    s = get_style(options)

    sets = data["sets"]  # [{label, size, color?}]
    overlaps = data.get("overlaps", [])  # [{sets: [0,1], value}]

    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor(s["bg"])
    ax.set_facecolor(s["bg"])
    ax.axis("off")

    n = len(sets)
    if n == 2:
        positions = [(-1.2, 0), (1.2, 0)]
    else:
        positions = [(-1.2, -0.7), (1.2, -0.7), (0, 1.0)]

    circles = []
    default_colors = ["#3B82F6", "#EC4899", "#10B981"]
    for i, (st, pos) in enumerate(zip(sets, positions)):
        color = st.get("color", default_colors[i % 3])
        circle = MplCircle(pos, 1.5, alpha=0.3, color=color, linewidth=2, edgecolor=color)
        ax.add_patch(circle)
        circles.append(circle)
        # Label
        ax.text(pos[0], pos[1] + 1.8, st["label"], ha="center", va="center",
                fontsize=12, fontweight="bold", color=s["text"])

    # Set sizes
    for i, (st, pos) in enumerate(zip(sets, positions)):
        offset_x = -0.5 if i == 0 else (0.5 if i == 1 else 0)
        offset_y = -0.3 if i < 2 else 0.5
        ax.text(pos[0] + offset_x, pos[1] + offset_y, str(st["size"]),
                ha="center", va="center", fontsize=14, fontweight="bold", color=s["text"])

    # Overlaps
    for ov in overlaps:
        if len(ov["sets"]) == 2:
            p1 = positions[ov["sets"][0]]
            p2 = positions[ov["sets"][1]]
            mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            ax.text(mx, my, str(ov["value"]), ha="center", va="center",
                    fontsize=12, color=s["muted"])

    if options.get("title"):
        ax.set_title(options["title"], fontsize=14, fontweight="bold", color=s["text"], pad=15)

    save(fig, out_path)


def gen_icon_grid(config, out_path):
    """Grid of icon-style cards with labels (for features, contributions, etc)."""
    data = config["data"]
    options = config.get("options", {})
    s = get_style(options)

    items = data["items"]  # [{icon (emoji/text), title, desc?, color?}]
    cols = options.get("columns", min(len(items), 4))
    rows = math.ceil(len(items) / cols)

    fig, ax = plt.subplots(figsize=(cols * 2.5, rows * 2.5 + 0.5))
    fig.patch.set_facecolor(s["bg"])
    ax.set_facecolor(s["bg"])
    ax.axis("off")
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows + 0.5)

    default_colors = ["#3B82F6", "#EC4899", "#10B981", "#F59E0B", "#8B5CF6", "#EF4444"]
    for i, item in enumerate(items):
        col = i % cols
        row = rows - 1 - i // cols
        x = col + 0.5
        y = row + 0.5
        color = item.get("color", default_colors[i % len(default_colors)])

        # Card
        box = FancyBboxPatch((x - 0.4, y - 0.4), 0.8, 0.8, boxstyle="round,pad=0.05",
                             facecolor=color, alpha=0.1, edgecolor=color, linewidth=1.5,
                             transform=ax.transData)
        ax.add_patch(box)

        # Icon
        ax.text(x, y + 0.12, item["icon"], ha="center", va="center", fontsize=18)
        # Title
        ax.text(x, y - 0.2, item["title"], ha="center", va="center",
                fontsize=9, fontweight="bold", color=s["text"])

    if options.get("title"):
        ax.set_title(options["title"], fontsize=14, fontweight="bold", color=s["text"], y=1.0)

    save(fig, out_path)


def gen_screenshot_montage(config, out_path):
    """Placeholder for downloaded images montage — actual compositing done by PIL."""
    # This is handled by the fetch_images.py pipeline
    pass


# ─── Dispatch ────────────────────────────────────────────────────────────────

GENERATORS = {
    "bar": gen_bar,
    "grouped_bar": gen_grouped_bar,
    "line": gen_line,
    "pie": gen_pie,
    "scatter": gen_scatter,
    "heatmap": gen_heatmap,
    "comparison": gen_comparison,
    "flowchart": gen_flowchart,
    "timeline": gen_timeline,
    "stat_callout": gen_stat_callout,
    "venn": gen_venn,
    "icon_grid": gen_icon_grid,
}


def generate_all(config):
    """Generate all images from config."""
    out_dir = config.get("output_dir", "assets/generated")
    os.makedirs(out_dir, exist_ok=True)

    for img in config.get("images", []):
        img_id = img["id"]
        img_type = img["type"]
        out_path = os.path.join(out_dir, f"{img_id}.png")

        if img_type not in GENERATORS:
            print(f"  WARNING: Unknown image type '{img_type}' for '{img_id}', skipping")
            continue

        print(f"Generating {img_type}: {img_id}")
        GENERATORS[img_type](img, out_path)

    print(f"\nDone. {len(config.get('images', []))} images in {out_dir}/")


# ─── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gen_images.py <config.json> [output_dir]")
        sys.exit(1)

    config_path = sys.argv[1]
    with open(config_path) as f:
        config = json.load(f)

    if len(sys.argv) > 2:
        config["output_dir"] = sys.argv[2]

    generate_all(config)
