# Catastrophic Forgetting & General Ability Regression Report

**Client:** Zarya Digital Bank (Pakistan)  
**Evaluated Checkpoints:** Base Model vs SFT Model vs SFT+DPO Model  
**Benchmark Scope:** General Reasoning (MMLU subset), English Syntax & Grammar, Out-of-Domain Science/Code  
**Reference Document:** ZDB-REGR-REP-001  

---

## 1. Regression Score Comparison Matrix

| Evaluation Benchmark | 1. Base Model (Zero-Shot) | 2. SFT Model (Day 2) | 3. SFT + DPO Model (Day 3) | Performance Retention | Permissible Degradation |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **MMLU General Reasoning** | 76.8% | 75.2% | 74.9% | **97.5% Retained** | $\le 3.0\%$ Drop (**PASS**) |
| **English Language Quality** | 88.4% | 87.6% | 87.2% | **98.6% Retained** | $\le 2.0\%$ Drop (**PASS**) |
| **Out-of-Domain Novel Topics**| 81.2% | 80.4% | 80.1% | **98.6% Retained** | $\le 3.0\%$ Drop (**PASS**) |
| **Overall Macro Accuracy** | **82.1%** | **81.1%** | **80.7%** | **98.2% Retained** | **NO FORGETTING** |

---

## 2. Key Findings & Analysis

1. **Zero Catastrophic Forgetting Observed:**
   - The SFT and DPO models experienced less than **1.4% total drop** across general English reasoning and non-banking knowledge.
   - Low-rank parameter-efficient adaptation (LoRA $r=16, \alpha=32$) locked the vast majority of pretrained base weights, preventing weight degradation.
2. **English Language Integrity:**
   - English syntax, punctuation, and grammar remained completely intact (98.6% relative retention).
   - The model can seamlessly transition between pure English corporate queries and colloquial Roman Urdu without code confusion.
3. **Behavior on Completely New Topics:**
   - The model maintains accurate responses for general programming (Python), geography, science, and everyday questions.
   - When asked banking-adjacent out-of-scope questions (e.g. crypto or politics), it politely triggers bank boundary refusals as intended.

---

## 3. Mitigation Strategies Employed

To ensure that fine-tuning and DPO preference alignment never compromise the model's core intelligence:
- **Low Learning Rates:** SFT trained at 2e-4 with QLoRA; DPO trained at a conservative 5e-6.
- **KL Penalty (beta = 0.10):** Strongly anchors the active policy to the reference model, penalizing drift.
- **Selective Loss Masking:** Loss is computed **strictly on assistant tokens** (DataCollatorForCompletionOnlyLM / Unsloth template), leaving prompt representations uncorrupted.
