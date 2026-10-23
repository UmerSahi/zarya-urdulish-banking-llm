# Week 10 Capstone Project — Zarya Digital Bank (UrduLish LLM)

## Day 1: Problem Framing & Dataset Engineering

All work for Day 1 has been executed and organized in the dedicated folder:
📂 [`problem_framing_and_dataset_engineering`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering)

### Overview of Completed Tasks

| Task | Title | Description | Key Deliverables |
| :--- | :--- | :--- | :--- |
| **Task 1** | **Fine-Tune vs Prompt vs RAG** | Architectural decision document comparing quality, cost, privacy, latency, and updates. Justifies hybrid approach under State Bank of Pakistan (SBP) regulations. | [`decision_document.md`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/decision_document.md) |
| **Task 2** | **Data Specification** | Full specification of ChatML/Llama-3 formats, task distribution, UrduLish tone guide, and Pydantic schema for automated support tickets. | [`data_specification.md`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/data_specification.md)<br>[`schemas.py`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/schemas.py) |
| **Task 3** | **Synthetic Data Generation** | 100+ hand-crafted seeds expanded into 6,800 synthetic banking conversations across 5 personas, dynamic Pakistani entities, and typo models. | [`seed_data.py`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/seed_data.py)<br>[`generate_dataset.py`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/generate_dataset.py)<br>[`generation_documentation.md`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/generation_documentation.md) |
| **Task 4** | **Data Quality & Cleaning** | Multi-stage cleaning pipeline: exact deduplication, length filters, Pydantic schema validation, Pakistani banking PII scan/redaction, and TF-IDF near-deduplication. Includes 200-sample human review CSV and interactive HTML review app. | [`clean_dataset.py`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/clean_dataset.py)<br>[`human_review_tool.py`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/human_review_tool.py)<br>[`human_review_app.html`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/data/human_review_app.html)<br>[`cleaning_report.md`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/reports/cleaning_report.md) |
| **Task 5** | **Splits, Test Set & Data Card** | Created training split (2,719 examples), validation split (302 examples), and a separate 200-example Golden Test Set held out exclusively for Day 2–5 evaluation. Generated official Hugging Face dataset card and upload script. | [`split_and_prep.py`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/split_and_prep.py)<br>[`DATASET_CARD.md`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/DATASET_CARD.md)<br>[`upload_to_hf.py`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/upload_to_hf.py)<br>[`train.jsonl`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/data/train.jsonl)<br>[`golden_test_set.jsonl`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/problem_framing_and_dataset_engineering/data/golden_test_set.jsonl) |

---

### Quick Start / Reproduction

To re-run the entire Day 1 pipeline end-to-end:
```bash
python problem_framing_and_dataset_engineering/run_pipeline.py
```

---

## Day 3: Evaluation Framework & Preference Alignment (DPO)

All work for Day 3 has been executed and organized in the dedicated folder:
📂 [`evaluation_framework_and_preference_alignment`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment)

### Overview of Day 3 Deliverables

| Task | Title | Description | Key Deliverables |
| :--- | :--- | :--- | :--- |
| **Task 1** | **Evaluation Harness** | Automated benchmark scoring Intent/Category accuracy & Macro F1, JSON validity, safety refusal rate, policy faithfulness, and 1-5 LLM-as-a-judge scoring calibrated with human agreement. | [`evaluation_harness.py`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/evaluation_harness.py)<br>[`llm_judge_rubric.md`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/llm_judge_rubric.md)<br>[`evaluation_report.md`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/reports/evaluation_report.md) |
| **Task 2** | **Blind Human Evaluation** | 50 triple-blinded questions evaluated across 3 models (Base vs SFT vs API). Analyzes win rates and qualitative UrduLish tone/fluency. Includes interactive HTML viewer. | [`human_evaluation_tool.py`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/human_evaluation_tool.py)<br>[`blind_eval_app.html`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/data/blind_eval_app.html)<br>[`blind_human_eval_report.md`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/reports/blind_human_eval_report.md) |
| **Task 3** | **Preference Dataset (DPO)** | 650 high-quality pairwise preference samples (`prompt`, `chosen`, `rejected`) teaching safety refusals, authentic UrduLish, and zero policy hallucination. Split into train (585) and val (65). | [`dpo_dataset_generator.py`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/dpo_dataset_generator.py)<br>[`dpo_train.jsonl`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/data/dpo_train.jsonl)<br>[`dpo_val.jsonl`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/data/dpo_val.jsonl) |
| **Task 4** | **DPO Theory & Colab Training** | In-depth derivation of Direct Preference Optimization (Bradley-Terry formulation, beta tuning, reward margins) plus a ready-to-run Google Colab Notebook with step-by-step instructions. | [`dpo_theory_and_formulation.md`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/dpo_theory_and_formulation.md)<br>[`DPO_Training_Colab.ipynb`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/DPO_Training_Colab.ipynb)<br>[`colab_instructions.md`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/colab_instructions.md) |
| **Task 5** | **Regression & Forgetting Checks** | Evaluates retention across MMLU reasoning, English grammar, and novel out-of-domain topics. Confirms 98.2% general retention (no catastrophic forgetting). | [`forgetting_and_regression_checks.py`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/forgetting_and_regression_checks.py)<br>[`catastrophic_forgetting_report.md`](file:///c:/Users/PMYLS/Downloads/Fine%20Tune%20Banking%20LLM/evaluation_framework_and_preference_alignment/reports/catastrophic_forgetting_report.md) |

---

### Running Day 3 Locally:
```bash
python evaluation_framework_and_preference_alignment/run_day3_pipeline.py
```

