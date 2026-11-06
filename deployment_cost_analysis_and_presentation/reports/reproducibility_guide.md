# End-to-End Training & Evaluation Reproducibility Guide

**Client:** Zarya Digital Bank (Pakistan)  
**Task:** Week 10 Capstone — Day 5 Task 5  
**Hardware Tested:** Google Colab Free Tesla T4 GPU (16GB VRAM) & Local AVX2 CPU  

---

## 1. Environment Setup

Clone repository and install dependencies:
```bash
git clone https://github.com/zarya-digital-bank/banking-llm.git
cd banking-llm
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 2. Day 1: Dataset Generation & Cleaning Pipeline

To reproduce the 6,800 synthetic banking conversations, PII sanitization, and dataset splitting:
```bash
python problem_framing_and_dataset_engineering/run_pipeline.py
```
This executes:
1. `seed_data.py`: Loads 100+ authentic Pakistani banking seed conversations.
2. `generate_dataset.py`: Expands seeds into diverse personas with typo models.
3. `clean_dataset.py`: Deduplicates (exact + TF-IDF) and runs Presidio PII scans.
4. `split_and_prep.py`: Generates `train.jsonl` (2,719), `val.jsonl` (302), and `golden_test_set.jsonl` (200).

---

## 3. Day 2: Supervised Fine-Tuning (SFT with QLoRA)

Using Unsloth on Google Colab or Kaggle:
1. Open [`Adaptors/Unsloth_Studio_Colab.ipynb`](file:///Adaptors/Unsloth_Studio_Colab.ipynb).
2. Configure base model: `unsloth/Qwen2.5-3B-Instruct-unsloth-bnb-4bit`.
3. Set LoRA hyper-parameters:
   - Rank: $r = 16$
   - Alpha: $\alpha = 32$
   - Target modules: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
   - Learning rate: $2 \times 10^{-4}$ with linear warmup
   - Batch size: 2 with gradient accumulation steps 4
   - Epochs: 3
4. Run training and export adapter weights to `Adaptors/qwen-adaptors/`.

---

## 4. Day 3: DPO Alignment & Evaluation Framework

1. **Generate DPO Preference Pairs:**
   ```bash
   python evaluation_framework_and_preference_alignment/dpo_dataset_generator.py
   ```
2. **Execute Evaluation Benchmark:**
   ```bash
   python evaluation_framework_and_preference_alignment/evaluation_harness.py
   ```
3. **Verify Zero Catastrophic Forgetting:**
   ```bash
   python evaluation_framework_and_preference_alignment/forgetting_and_regression_checks.py
   ```

---

## 5. Day 4: Quantization, Serving & RAG System

1. **Benchmark Model Quantization (FP16 vs INT8 vs INT4):**
   ```bash
   python quantization_serving_rag_hybrid_and_guardrails/quantize_and_benchmark.py
   ```
2. **Execute High-Throughput Load Testing:**
   ```bash
   python quantization_serving_rag_hybrid_and_guardrails/load_test.py
   ```
3. **Test Zero-Retraining Hybrid RAG Document Update:**
   ```bash
   python quantization_serving_rag_hybrid_and_guardrails/rag_system.py
   ```

---

## 6. Day 5: Production Deployment & Serving

1. **Launch FastAPI Serving Gateway:**
   ```bash
   uvicorn deployment_cost_analysis_and_presentation.api_server:app --host 0.0.0.0 --port 8000 --reload
   ```
2. **Launch Streamlit Chatbot & CRM Dashboard:**
   ```bash
   streamlit run deployment_cost_analysis_and_presentation/app.py
   ```
3. **Run Continuous Feedback Pipeline:**
   ```bash
   python deployment_cost_analysis_and_presentation/feedback_pipeline.py
   ```
4. **Push Release to Hugging Face Hub:**
   ```bash
   python deployment_cost_analysis_and_presentation/push_to_hf.py --token <YOUR_HF_TOKEN>
   ```

