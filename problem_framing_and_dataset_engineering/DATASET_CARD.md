---
language:
- ur
- en
license: apache-2.0
tags:
- banking
- fintech
- urdulish
- roman-urdu
- pakistan
- customer-support
- conversational
- safety-alignment
- structured-output
pretty_name: Zarya Digital Bank UrduLish Support Dataset (ZDB-UrduLish-v1)
size_categories:
- 1K<n<10K
task_categories:
- text-generation
- conversational
---

# Dataset Card for Zarya Digital Bank UrduLish Assistant (ZDB-UrduLish-v1)

## 1. Dataset Summary

**ZDB-UrduLish-v1** is a specialized instruction-tuning and conversational dataset curated for training open-source financial LLMs (e.g., Qwen 2.5 3B/7B, Llama 3.2 3B) for retail banking in Pakistan. Developed specifically for **Zarya Digital Bank (fictional)**, the dataset addresses the real-world linguistic realities of Pakistani digital banking customers who communicate predominantly in **UrduLish** (Roman Urdu code-switched with English financial terms).

The dataset emphasizes:
1. **Pakistani Retail Banking Scenarios:** Comprehensive coverage of Raast P2P/P2M payments, 1Link IBFT transfers, ATM cash disputes, card blocking, dormancy, digital nano-loans, and utility bill settlements.
2. **State Bank of Pakistan (SBP) Compliance:** Accurate turnaround times (TAT), complaint handling protocols, and strict adherence to SBP BPRD consumer protection circulars.
3. **Hardened Security & Anti-Fraud Reflexes:** Dedicated refusal trajectories rejecting requests for OTPs, ATM MPINs, card CVVs, and passwords, accompanied by prompt warnings against social engineering scam calls.
4. **Structured JSON Triage:** Emits valid JSON payloads for automated ticketing and queue routing in core banking systems.

---

## 2. Dataset Structure

### 2.1 File Splits

| Split | File Name | Size (Records) | Description |
| :--- | :--- | :--- | :--- |
| **Train** | `data/train.jsonl` | **2,719** | Primary supervised fine-tuning (SFT) training split. |
| **Validation** | `data/val.jsonl` | **302** | Validation split for checkpoint evaluation and loss tracking. |
| **Golden Test** | `data/golden_test_set.jsonl` | **200** | Curated benchmark set held out exclusively for Day 2–5 evaluation; never used in training. |
| **Total** | — | **3,221** | 100% clean, deduplicated, and PII-redacted records. |

### 2.2 Data Fields

Each JSONL record represents a conversation object conforming to the standard chat format:
```json
{
  "id": "ZDB-EXP-00142",
  "task_type": "faq | complaint | fraud_refusal | multi_turn | structured_json",
  "category": "transfers_payments | cards_atm | account_balance | loans_products | complaints_disputes | fraud_security | out_of_scope",
  "language": "urdulish | roman_urdu | english | mixed",
  "is_multi_turn": true,
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "metadata": {
    "intent": "raast_transfer_failed",
    "sub_category": "raast_p2p_failure",
    "persona": "panicked_merchant",
    "tat_hours": 24
  }
}
```

---

## 3. Task & Category Distribution

### 3.1 Category Mix
- **Transfers & Payments (`transfers_payments`):** ~28.5% (Raast failure, IBFT delay, wrong IBAN recall, bill payment sync)
- **Cards & ATM (`cards_atm`):** ~23.2% (Lost card block, ATM cash not dispensed, swallowed card, international e-commerce activation)
- **Fraud & Security Scams (`fraud_security`):** ~14.8% (Fake bank manager calls, OTP phishing links, unauthorized debit dispute)
- **Account & Balance Services (`account_balance`):** ~12.5% (Dormancy lift, digital visa statements, biometric verification, balance holds)
- **Complaints & Escalations (`complaints_disputes`):** ~10.2% (TAT breach escalations, annual card fee clarifications, agent overcharge)
- **Loans & Products (`loans_products`):** ~5.8% (Nano loan eligibility, PLS savings profit rate calculation, tax filer status)
- **Out of Scope (`out_of_scope`):** ~5.0% (Crypto ban refusal, cricket banter, medical refusal, politics)

### 3.2 Structural Targets Met
- **Multi-Turn Conversations:** **24.5%** of training set (Target: $\ge 20\%$)
- **Structured Output (JSON):** **421 examples** in train set (Target: $\ge 300$)
- **Safety, Fraud & Refusal Examples:** **440+ examples** across splits (Target: $\ge 300$)

---

## 4. Linguistic Distribution & Tone

- **UrduLish (Roman Urdu + English terms):** ~68%
- **Colloquial Pakistani Roman Urdu (slang & phonetic typos):** ~16%
- **Professional Banking English:** ~16%

### Persona Guidelines
- Addresses customer respectfully as *"Aap"*, *"Ji"*, or *"Janab"*.
- De-escalates anxiety on financial disputes (*"Pareshan na hon, aap ki raqam mehfooz hai"*).
- Concise replies (maximum 2 to 4 sentences).
- Zero tolerance for credential harvesting.

---

## 5. Data Curation & Quality Filtering

Prior to splitting, the dataset passed a 6-stage programmatic quality funnel:
1. **Exact Deduplication:** SHA-256 hash deduplication eliminated identical duplicate turns.
2. **Length Filters:** Enforced user length [8–800 characters] and assistant length [15–2000 characters].
3. **Pydantic Schema Validation:** 100% of structured JSON samples validated against `BankingSupportTicket`.
4. **Policy Guard:** Filtered any hallucinated crypto allowances or non-standard dispute turnaround times.
5. **PII Masking & Presidio Scanning:** Regex and pattern detectors masked all 13-digit Pakistani CNICs (`42101-*******-1`), 16-digit debit cards (`XXXX-XXXX-XXXX-1234`), CVVs, and IBANs.
6. **Near-Duplicate Pruning:** TF-IDF character and word n-gram cosine similarity (threshold $> 0.985$) pruned redundant prompt duplicates.

### Human Review Verification
A stratified random sample of 200 conversations was reviewed using `human_review_app.html` and logged in `human_review_sample.csv`, verifying a 99.5% quality pass rate and 0 PII leaks.

---

## 6. Known Limitations & Ethical Considerations

- **Synthetic Origin:** All customer names, account numbers, CNICs, and phone numbers are purely synthetic or safely redacted.
- **Regulatory Jurisdiction:** Turnaround times (TAT) and dispute procedures reflect Pakistani regulations governed by the State Bank of Pakistan (SBP) and may not apply to foreign jurisdictions.
- **Intended Use:** Designed strictly for training and evaluating automated banking customer service assistants and triage agents.
