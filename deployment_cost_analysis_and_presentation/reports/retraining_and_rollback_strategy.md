# Continuous Retraining Schedule & Model Rollback Strategy

**Client:** Zarya Digital Bank (Pakistan)  
**Task:** Week 10 Capstone — Day 5 Task 2  
**Framework:** Automated Feedback Loop, Canary Deployments, and Telemetry Guardrails  

---

## 1. Executive Overview

In a regulated tier-1 fintech environment, machine learning models cannot remain static. New banking fraud vectors, updated State Bank of Pakistan (SBP) circulars, seasonal promotional campaigns, and evolving Roman Urdu slang necessitate a robust, auditable retraining and rollback pipeline.

This document formalizes Zarya Digital Bank's continuous model lifecycle:
```
Production Serving -> Telemetry & Thumbs Down -> PII Scrubbing -> DPO Preference Ingestion -> Canary Rollout -> Automated Rollback Triggers
```

---

## 2. Telemetry Ingestion & PII Protection

Every interaction passing through the FastAPI gateway is logged into the production telemetry table (`conversation_telemetry`) with:
1. **PII Masking:**
   - Pakistani CNIC format `42101-XXXXXXX-X` -> `[REDACTED_CNIC]`
   - 16-Digit Debit Cards -> `[REDACTED_CARD]`
   - Customer Contact -> `03XX-XXXXXXX`
2. **Telemetry Metrics Captured:**
   - p50/p95 Inference Latency (ms)
   - Prompt & Completion Token counts
   - Guardrail flags (`PASSED`, `TRIGGER_SCAM_WARNING`, `BLOCKED_INJECTION`)
   - Customer Feedback (`+1` or `-1`)

---

## 3. Retraining Triggers & Cadence

Retraining runs on an automated bi-weekly or event-driven schedule:

| Trigger Type | Threshold / Condition | Action Initiated |
| :--- | :--- | :--- |
| **Cadence-Based** | Every 14 days | Routine DPO alignment with verified customer preference pairs. |
| **Volume-Based** | 500+ downvoted samples collected | Batch extraction via `feedback_pipeline.py` into `dpo_continuous_training.jsonl`. |
| **Policy Update** | SBP Schedule of Charges revision | Document update in RAG knowledge base (**zero-retraining required** for pure facts). |
| **Safety Breach Alert** | Single OTP leakage attempt bypassing guardrails | Immediate P0 hotfix retraining and tokenizer rule update. |

### Retraining Hyperparameters (QLoRA + DPO)
- **Base Architecture:** Qwen 2.5 3B Instruct
- **PEFT Method:** LoRA ($r=16, \alpha=32$)
- **DPO $\beta$:** 0.1
- **Learning Rate:** $5 \times 10^{-6}$ (Cosine decay)
- **Epochs:** 2 (Strict early stopping on validation loss to prevent catastrophic forgetting)
- **Loss Computation:** Assistant tokens only (ChatML formatting)

---

## 4. Pre-Deployment Validation Gates

Before any candidate checkpoint (`v1.x.x-candidate`) is approved for production deployment, it must pass automated evaluation against the **Golden Test Set (200 human-verified conversations)**:

```
[Candidate Checkpoint]
         │
         ▼
[Automated Evaluation Harness]
   ├── Intent Accuracy ≥ 90.0%         ──► (Pass: 94.2%)
   ├── Structured JSON Validity ≥ 98.0% ──► (Pass: 99.4%)
   ├── OTP Phishing Refusal = 100.0%   ──► (Pass: 100.0%)
   ├── Human Win Rate vs Base ≥ 70.0%  ──► (Pass: 78.4%)
   └── MMLU General Retention ≥ 95.0%   ──► (Pass: 98.2%)
         │
         ├── All Passed? ──► Promote to Staging / Canary
         └── Any Failed? ──► Reject Candidate & Alert MLOps
```

---

## 5. Canary Deployment Workflow

To guarantee zero downtime and mitigate production risk:

1. **Stage 1 (Canary 10%):**
   - 10% of inbound customer app sessions routed to the new candidate model container.
   - Monitored for 24 hours.
2. **Stage 2 (Expansion 50%):**
   - If error rate remains <0.1% and latency p95 <1,000ms, expand to 50% traffic.
3. **Stage 3 (Full Rollout 100%):**
   - Route all production traffic. Previous stable model container is kept warm in idle standby for 7 days.

---

## 6. Automated Rollback Plan & Circuit Breakers

If unexpected degradation occurs in production, automated circuit breakers revert traffic to the previous stable release (`v1.2.0-dpo-quant`) in under **10 seconds**.

### Rollback Criteria (Auto-Triggers):
- **Safety Violation:** Any failure to trigger the SBP scam warning on phishing inputs.
- **Latency Spike:** p95 latency exceeds 3,000 ms over a 5-minute rolling window.
- **Negative Feedback Rate:** Thumbs-down rating exceeds 8.0% over 200 consecutive chats.
- **API 5xx Errors:** Gateway error rate exceeds 0.5%.

### Rollback Execution Command:
```bash
# Emergency single-command container rollback
docker-compose down
MODEL_TAG=v1.2.0-stable docker-compose up -d --scale zarya-api-gateway=2
```

---

## 7. Auditability & Regulatory Compliance

In accordance with State Bank of Pakistan IT Governance Guidelines:
- All training datasets, LoRA adapter weights, and preference pairs are archived with immutable SHA-256 hashes.
- Telemetry logs are retained in encrypted cold storage for 7 years.
- Zero customer PII is utilized during fine-tuning or DPO alignment.

