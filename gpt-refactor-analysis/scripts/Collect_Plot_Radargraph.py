#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
from collections import Counter
import math
import matplotlib.pyplot as plt

# Five fixed categories (order determines clockwise order of radar chart axes)
CATEGORIES = [
    "DATA_PIPELINE",
    "MODEL_LOGIC",
    "TRAINING_PROCESS",
    "EVALUATION_MONITORING",
    "DEPLOYMENT_INFRASTRUCTURE",
]

KEY_NAME = "Component GPT4"  # The key in your JSON storing the classification result

def load_refactorings(path):
    """
    Support two possible JSON structures:
    1) Top level is a list of refactoring dicts
    2) Top level is a dict containing a key like 'refactorings' -> list
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        # Common structures: {"refactorings": [...]}, {"items": [...]}, {"data": [...]}, etc.
        for k in ("refactorings", "items", "data"):
            if k in data and isinstance(data[k], list):
                return data[k]

    # Fallback: if structure is unexpected, return empty list
    return []

def tally(refactorings):
    """
    Count occurrences of each category. Handle failures or unknown categories.
    """
    counts = Counter({c: 0 for c in CATEGORIES})
    total = len(refactorings)
    failed = 0

    for rf in refactorings:
        val = rf.get(KEY_NAME, None)

        # Allow val to be a string or a list (some files may store ["TRAINING_PROCESS"])
        if isinstance(val, list) and val:
            val = val[0]
        if isinstance(val, str):
            val = val.strip()

        if val in CATEGORIES:
            counts[val] += 1
        else:
            failed += 1

    return counts, total, failed

def plot_radar(counts, title, save_path):
    """
    Draw a pentagon-style radar chart based on category counts.
    """
    # Radar chart requires repeating the first value at the end to close the polygon
    values = [counts[c] for c in CATEGORIES]
    values.append(values[0])

    # Angles for each axis
    N = len(CATEGORIES)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles.append(angles[0])

    fig = plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)

    # Plot the line and fill (use default matplotlib colors)
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    # Axis labels
    ax.set_xticks([n / float(N) * 2 * math.pi for n in range(N)])
    ax.set_xticklabels(CATEGORIES)

    # Y-axis limits from 0 to an appropriate upper bound
    ymax = max(values) if values else 1
    if ymax == 0:
        ymax = 1
    ax.set_ylim(0, ymax)

    ax.set_title(title, pad=20)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close(fig)

def main():
    ap = argparse.ArgumentParser(description="Count RF categories and generate a pentagon radar chart.")
    ap.add_argument("json_file", help="Path to a project's JSON file")
    args = ap.parse_args()

    refactorings = load_refactorings(args.json_file)
    counts, total, failed = tally(refactorings)

    # Print statistics
    print(f"File: {args.json_file}")
    for c in CATEGORIES:
        print(f"{c}: {counts[c]}")
    print(f"TOTAL RFs: {total}")
    print(f"FAILED (unknown or missing '{KEY_NAME}'): {failed}")

    # Plot radar chart
    base = os.path.splitext(args.json_file)[0]
    out_png = f"{base}-radar.png"
    title = os.path.basename(args.json_file)
    plot_radar(counts, title, out_png)

    print(f"Radar chart saved to: {out_png}")

if __name__ == "__main__":
    main()
