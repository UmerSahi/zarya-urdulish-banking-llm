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
