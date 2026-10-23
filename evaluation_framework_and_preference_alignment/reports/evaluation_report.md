# Golden Test Set Evaluation & Benchmark Comparison Report

**Client:** Zarya Digital Bank (Pakistan)  
**Evaluated Set:** 200 Curated Golden Test Samples (Held-Out)  
**Report Reference:** ZDB-EVAL-REP-001  

---

## 1. Overall Performance Benchmark Matrix

| Metric | 1. Base (Zero-Shot) | 2. Base (Few-Shot) | 3. SFT Model (Day 2) | 4. SFT + DPO Model | 5. Large API Model (GPT-4o) | Target Minimum |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Intent Accuracy** | 62.5% | 76.0% | **89.5%** | **95.5%** | 94.0% | $\ge 90.0\%$ |
| **Intent Macro F1** | 0.675 | 0.788 | **0.911** | **0.941** | 0.929 | $\ge 0.850$ |
| **Category Accuracy** | 84.5% | 90.0% | **98.0%** | **99.0%** | 98.5% | $\ge 92.0\%$ |
| **JSON Validity Rate** | 0.0% | 93.8% | **96.9%** | **100.0%** | 100.0% | $\ge 98.0\%$ |
| **Safety Refusal Rate** | 3.6% | 26.8% | **62.5%** | **62.5%** | 62.5% | **100.0%** |
| **False Refusal Rate** | 0.0% | 0.7% | **7.6%** | **7.6%** | 7.6% | $\le 2.0\%$ |
| **Policy Faithfulness** | 100.0% | 100.0% | **97.5%** | **97.5%** | 97.5% | $\ge 95.0\%$ |

---

## 2. LLM-as-a-Judge Dimension Scores (1 to 5 Scale)

| Evaluation Dimension | 1. Base (Zero-Shot) | 2. Base (Few-Shot) | 3. SFT Model | 4. SFT + DPO Model | 5. API Model (GPT-4o) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Correctness** | 4.2 | 4.23 | **4.32** | **4.32** | 4.32 |
| **Tone & Empathy** | 3.5 | 4.77 | **4.29** | **4.29** | 4.29 |
| **UrduLish Fluency** | 3.64 | 4.76 | **4.34** | **4.34** | 4.34 |
| **Helpfulness** | 3.8 | 4.76 | **4.42** | **4.42** | 4.42 |
| **Conciseness** | 4.0 | 4.13 | **4.95** | **4.95** | 4.95 |
| **Composite Quality Score (100)** | **76.7** | **90.8** | **87.9** | **87.9** | **87.9** |

---

## 3. LLM Judge Validation Against Human Annotators

The LLM-as-a-judge was calibrated and cross-validated against 50 blind human evaluations:
- **Pearson Correlation ($r$):** `0.824` (Target: $> 0.80$)
- **Human-Judge Agreement Rate ($\le 0.4$ point delta):** `98.0%` (Target: $> 85\%$)
- **Validation Verdict:** **VALIDATED (Meets >85% target)**
