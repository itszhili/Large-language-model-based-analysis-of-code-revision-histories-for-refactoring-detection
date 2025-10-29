#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
from collections import Counter
import math
import matplotlib.pyplot as plt

# 五个固定类别（顺序会决定雷达图轴的顺时针排列）
CATEGORIES = [
    "DATA_PIPELINE",
    "MODEL_LOGIC",
    "TRAINING_PROCESS",
    "EVALUATION_MONITORING",
    "DEPLOYMENT_INFRASTRUCTURE",
]

KEY_NAME = "Component GPT4"  # 你的 JSON 中存放类别的键

def load_refactorings(path):
    """支持两种结构：
    1) 顶层是 list[refactoring_dict]
    2) 顶层是 dict 且含 'refactorings' -> list
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        # 常见：{"refactorings": [...]} 或 {"items":[...]} 之类
        for k in ("refactorings", "items", "data"):
            if k in data and isinstance(data[k], list):
                return data[k]
    # 兜底：如果结构不对，返回空列表
    return []

def tally(refactorings):
    counts = Counter({c: 0 for c in CATEGORIES})
    total = len(refactorings)
    failed = 0

    for rf in refactorings:
        val = rf.get(KEY_NAME, None)
        # 允许 val 为字符串或列表（有时存成 ["TRAINING_PROCESS"]）
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
    # 雷达图需要把第一个点重复到末尾闭合
    values = [counts[c] for c in CATEGORIES]
    values.append(values[0])

    # 角度
    N = len(CATEGORIES)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles.append(angles[0])

    fig = plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)

    # 画线与填充（不指定颜色，使用默认）
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    # 轴标签
    ax.set_xticks([n / float(N) * 2 * math.pi for n in range(N)])
    ax.set_xticklabels(CATEGORIES)

    # y 轴从 0 到最大计数的合适上界
    ymax = max(values) if values else 1
    if ymax == 0:
        ymax = 1
    ax.set_ylim(0, ymax)

    ax.set_title(title, pad=20)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close(fig)

def main():
    ap = argparse.ArgumentParser(description="Count RF categories and draw a pentagon radar chart.")
    ap.add_argument("json_file", help="Path to a project's JSON file")
    args = ap.parse_args()

    refactorings = load_refactorings(args.json_file)
    counts, total, failed = tally(refactorings)

    # 打印统计
    print(f"File: {args.json_file}")
    for c in CATEGORIES:
        print(f"{c}: {counts[c]}")
    print(f"TOTAL RFs: {total}")
    print(f"FAILED (unknown/missing '{KEY_NAME}'): {failed}")

    # 画图
    base = os.path.splitext(args.json_file)[0]
    out_png = f"{base}-radar.png"
    title = os.path.basename(args.json_file)
    plot_radar(counts, title, out_png)
    print(f"Radar chart saved to: {out_png}")

if __name__ == "__main__":
    main()
