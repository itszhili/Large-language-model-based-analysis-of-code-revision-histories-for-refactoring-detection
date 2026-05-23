# LLM-Based Analysis of Code Revision Histories for Refactoring Detection

A research project that leverages Large Language Models (LLMs) — including **GPT-4** and **LLaMA 2** — to detect and classify software refactorings in Python project revision histories.

---

## Overview

This project combines static analysis with LLM-based classification to study refactoring patterns in open-source Python machine learning projects. The pipeline consists of three main stages:

1. **Refactoring Detection** — Extract refactoring operations from Git commit histories using [PyRef](https://github.com/PyRef/PyRef).
2. **LLM Classification** — Classify each detected refactoring using GPT-4 or LLaMA 2 into ML-specific components or general software categories.
3. **Evaluation & Visualization** — Compute precision/recall/F1 metrics and visualize category distributions with radar charts.

---

## Repository Structure

```
.
├── PyRef/                          # Refactoring detection engine
│   ├── main.py                     # CLI entry point
│   ├── requirements.txt
│   ├── preprocessing/              # AST-based diff analysis
│   │   ├── refactorings.py         # Refactoring data classes
│   │   ├── diff_list.py            # Diff extraction logic
│   │   ├── refactoring_heuristics.py
│   │   └── ...
│   └── data/
│       └── dataset.csv             # Labeled oracle dataset
│
├── llama/                          # LLaMA 2 classification module
│   ├── Add_classification.py       # One-shot classification with LLaMA
│   ├── Add_classification_for_all.py
│   ├── Add_classification_for_graph.py
│   ├── Add_classification_short.py
│   ├── requirements.txt
│   └── llama-2-7b[-chat]/          # Model weights (not included)
│
└── gpt-refactor-analysis/          # GPT-4 classification & analysis
    ├── scripts/
    │   ├── Detection.py            # Batch refactoring detection
    │   ├── Ask_GPT4.py             # Binary classification (ML-specific vs General)
    │   ├── Ask_GPT4_graph.py       # Component-level classification
    │   ├── Ask_GPT4_graph_list.py  # Batch graph classification
    │   ├── Compute_matrix.py       # Precision / Recall / F1 evaluation
    │   ├── Collect_Plot_Radargraph.py  # Radar chart generation
    │   ├── collect_30_dataset.py   # Dataset sampling utility
    │   ├── commit.py               # Commit-level analysis
    │   ├── count_refactorings.py
    │   ├── Label_Category.py
    │   └── ...
    ├── dataset/                    # Per-project JSON refactoring data
    │   └── *_data.json / *_GPT4_component_graph.json
    └── figures/                    # Generated radar charts
        └── *-radar.png
```

---

## Modules

### 1. PyRef — Refactoring Detection

PyRef detects method-level refactoring operations in Python projects by analyzing AST-level diffs between consecutive commits.

**Supported refactoring types:**

| Refactoring Type        | Description                              |
|-------------------------|------------------------------------------|
| Rename Method           | Method is renamed                        |
| Add Parameter           | Parameter(s) added to a method           |
| Remove Parameter        | Parameter(s) removed from a method       |
| Change/Rename Parameter | Parameter names changed                  |
| Extract Method          | Code extracted into a new method         |
| Inline Method           | Method body inlined into caller          |
| Move Method             | Method moved to another class/module     |
| Pull Up Method          | Method moved to a parent class           |
| Push Down Method        | Method moved to a child class            |

**Output format** (`<project>_data.json`):
```json
[
  {
    "Refactoring Type": ["Add Parameter"],
    "Original": "method_name",
    "Updated": "method_name",
    "Location": "path/to/module.py/ClassName",
    "Original Line": 42,
    "Updated Line": 45,
    "Description": ["The parameters [ x ] are added to the method ..."],
    "Commit": "abc123..."
  }
]
```

### 2. LLM Classification

Detected refactorings are sent to an LLM for classification. Two classification schemes are supported:

#### Binary Classification
- **ML-Specific** — Refactoring relates to machine learning functionality
- **General** — Standard software engineering refactoring

#### Component-Level Classification (Graph)
Refactorings are classified into one of the following ML pipeline components:

| Category                   | Description                                  |
|----------------------------|----------------------------------------------|
| `DATA_PIPELINE`            | Data loading, preprocessing, augmentation   |
| `MODEL_LOGIC`              | Model architecture and layers                |
| `TRAINING_PROCESS`         | Training loops, optimizers, schedulers       |
| `EVALUATION_MONITORING`    | Metrics, validation, logging                 |
| `DEPLOYMENT_INFRASTRUCTURE`| Serving, export, deployment utilities        |

#### Supported LLMs
- **GPT-4** via OpenAI API (`gpt-refactor-analysis/scripts/Ask_GPT4*.py`)
- **LLaMA 2** (7B / 7B-Chat) via local inference (`llama/Add_classification*.py`)

---

## Getting Started

### Prerequisites

- Python 3.8+
- Git

### Installation

**PyRef dependencies:**
```bash
cd PyRef
pip install -r requirements.txt
```
> ⚠️ Requires `pandas < 2.0.0` (the `.append()` API is used internally).

**LLaMA dependencies:**
```bash
cd llama
pip install -r requirements.txt
```

**GPT-4 analysis dependencies:**
```bash
pip install openai python-dotenv fire pandas matplotlib
```

---

## Usage

### Step 1: Detect Refactorings with PyRef

Clone a target repository:
```bash
cd PyRef
python3 main.py repoClone -u "owner" -r "repo-name"
```

Extract refactorings from the cloned repository:
```bash
python3 main.py getrefs -r "Repos/repo-name"
```

Optional flags:
```bash
# Skip commits that take longer than N minutes
python3 main.py getrefs -r "Repos/repo-name" -s 10

# Analyze a specific commit
python3 main.py getrefs -r "Repos/repo-name" -c "<commit-hash>"

# Analyze a specific directory
python3 main.py getrefs -r "Repos/repo-name" -d "src/"
```

Results are saved to `<repo-name>_data.json`.

### Step 2: Batch Detection Across Multiple Projects

Edit paths in `gpt-refactor-analysis/scripts/Detection.py`, then run:
```bash
python Detection.py
```

This reads a CSV list of repositories and runs PyRef on each, skipping projects whose JSON output already exists.

### Step 3: Classify Refactorings with GPT-4

Set your OpenAI API key in a `.env` file:
```
OPENAI_API_KEY=your_key_here
```

Run binary classification:
```bash
cd gpt-refactor-analysis/scripts
python Ask_GPT4.py
```

Run component-level (graph) classification:
```bash
python Ask_GPT4_graph.py
```

### Step 4: Classify with LLaMA 2

Ensure LLaMA 2 weights are placed in `llama/llama-2-7b-chat/`.

Run with `torchrun`:
```bash
cd llama
torchrun --nproc_per_node 1 Add_classification.py \
    --ckpt_dir llama-2-7b-chat/ \
    --tokenizer_path tokenizer.model \
    --max_seq_len 512 \
    --max_batch_size 8
```

### Step 5: Evaluate Classification Quality

```bash
cd gpt-refactor-analysis/scripts
python Compute_matrix.py
```

Outputs:
```
True Positive (TP): ...
False Positive (FP): ...
True Non-ML-Specific (TN): ...
False Negative (FN): ...

Precision: 0.XXXX
Recall:    0.XXXX
F1 score:  0.XXXX
```

### Step 6: Generate Radar Charts

```bash
python Collect_Plot_Radargraph.py path/to/project_data_GPT4_component_graph.json
```

A pentagon radar chart will be saved as `<project>-radar.png` in the same directory.

---

## Dataset

The `gpt-refactor-analysis/dataset/` directory contains refactoring data extracted from 30+ open-source Python ML projects, including:

- `ultralytics`, `whisper-timestamped`, `tutor-gpt`, `torchcde`
- `texar-pytorch`, `uis-rnn`, `verde`, `zi2zi`, and more

Each project has two JSON files:
- `<project>_data.json` — raw detected refactorings
- `<project>_data_GPT4_component_graph.json` — GPT-4 component classifications

---

## Related Work

**PyRef** was originally published in:

> H. Atwi, B. Lin, N. Tsantalis, Y. Kashiwa, Y. Kamei, N. Ubayashi, G. Bavota and M. Lanza,
> *"PyRef: Refactoring Detection in Python Projects,"*
> IEEE 21st International Working Conference on Source Code Analysis and Manipulation (SCAM), 2021.

---

## License

- **PyRef** is licensed under its original license (see `PyRef/LICENSE`).
- **LLaMA 2** is subject to Meta's [Llama 2 Community License](https://ai.meta.com/llama/license/).
- All other scripts in this repository are for research purposes.
