"""
Dataset Splitting, Golden Test Set Extraction & Data Preparation Pipeline
Client: Zarya Digital Bank (Pakistan)
Task: Task 5 — Splits, Test Set & Data Card
"""

import os
import json
import random
from typing import List, Dict, Any

from schemas import TicketCategory, TicketUrgency, CustomerSentiment

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

def prepare_splits_and_golden_test(clean_dataset_path: str, golden_size: int = 200, val_ratio: float = 0.10):
    print(f"Loading cleaned dataset from {clean_dataset_path}...")
    with open(clean_dataset_path, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    total_records = len(records)
    print(f"Total available cleaned records: {total_records}")

    random.seed(42)
    random.shuffle(records)

    # 1. Stratified Extraction of the Golden Test Set (200 Curated, Human-Verified Examples)
    # Stratify by category to ensure balanced coverage
    by_category = {}
    for r in records:
        cat = r["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(r)

    golden_set = []
    # Quotas for golden set
    golden_targets = {
        "transfers_payments": 45,
        "cards_atm": 40,
        "fraud_security": 40,
        "account_balance": 30,
        "complaints_disputes": 25,
        "loans_products": 10,
        "out_of_scope": 10
    }

    golden_ids = set()
    for cat, target_n in golden_targets.items():
        available = by_category.get(cat, [])
        sampled_cat = available[:target_n]
        for it in sampled_cat:
            golden_set.append(it)
            golden_ids.add(it["id"])

    # If any remaining needed to reach exactly 200
    if len(golden_set) < golden_size:
        remaining_pool = [r for r in records if r["id"] not in golden_ids]
        needed = golden_size - len(golden_set)
        for it in remaining_pool[:needed]:
            golden_set.append(it)
            golden_ids.add(it["id"])
    elif len(golden_set) > golden_size:
        golden_set = golden_set[:golden_size]
        golden_ids = set(it["id"] for it in golden_set)

    print(f"Extracted Golden Test Set: {len(golden_set)} examples (NEVER used in training)")

    # 2. Split Remaining Data into Train and Validation
    train_val_pool = [r for r in records if r["id"] not in golden_ids]
    random.shuffle(train_val_pool)

    n_val = int(len(train_val_pool) * val_ratio)
    val_set = train_val_pool[:n_val]
    train_set = train_val_pool[n_val:]

    print(f"Training Split:   {len(train_set)} examples")
    print(f"Validation Split: {len(val_set)} examples")
    print(f"Golden Test Split:{len(golden_set)} examples")
    print(f"Total Preserved:  {len(train_set) + len(val_set) + len(golden_set)} examples")

    # 3. Write Split Files
    train_path = os.path.join(DATA_DIR, "train.jsonl")
    val_path = os.path.join(DATA_DIR, "val.jsonl")
    golden_path = os.path.join(DATA_DIR, "golden_test_set.jsonl")

    with open(train_path, "w", encoding="utf-8") as f:
        for it in train_set:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

    with open(val_path, "w", encoding="utf-8") as f:
        for it in val_set:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

    with open(golden_path, "w", encoding="utf-8") as f:
        for it in golden_set:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

    print(f"Saved: {train_path}")
    print(f"Saved: {val_path}")
    print(f"Saved: {golden_path}")

    # 4. Compute Statistical Summary for Data Card
    def compute_stats(dataset):
        categories = {}
        languages = {}
        multi_turn = sum(1 for it in dataset if it.get("is_multi_turn", False))
        json_tasks = sum(1 for it in dataset if it.get("task_type") == "structured_json")
        for it in dataset:
            c = it["category"]
            categories[c] = categories.get(c, 0) + 1
            l = it.get("language", "urdulish")
            languages[l] = languages.get(l, 0) + 1
        return {
            "total": len(dataset),
            "multi_turn": multi_turn,
            "multi_turn_pct": f"{multi_turn / len(dataset):.1%}",
            "structured_json": json_tasks,
            "categories": categories,
            "languages": languages
        }

    summary = {
        "train": compute_stats(train_set),
        "validation": compute_stats(val_set),
        "golden_test": compute_stats(golden_set)
    }

    stat_report_path = os.path.join(REPORTS_DIR, "dataset_analysis_report.json")
    with open(stat_report_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


if __name__ == "__main__":
    clean_file = os.path.join(DATA_DIR, "cleaned_dataset.jsonl")
    summary = prepare_splits_and_golden_test(clean_file, golden_size=200, val_ratio=0.10)
    print("\n--- Split Statistics Summary ---")
    print(f"Train Count: {summary['train']['total']} | Multi-Turn: {summary['train']['multi_turn_pct']} | JSON: {summary['train']['structured_json']}")
    print(f"Val Count:   {summary['validation']['total']}")
    print(f"Golden Count:{summary['golden_test']['total']}")
