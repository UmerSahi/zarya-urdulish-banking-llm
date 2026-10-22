# Architectural Decision Document: Fine-Tuning vs. Prompting vs. RAG

**Client:** Zarya Digital Bank (Fictional Pakistani Digital Retail Bank)  
**Scale:** 2 Million Active App Users | ~50,000 Inbound Customer Support Queries / Day  
**Language Environment:** UrduLish (Roman Urdu + English code-switching), Formal Roman Urdu, English  
**Regulatory Context:** State Bank of Pakistan (SBP) Framework for Digital Banking, BPRD Circulars on Customer Data Protection and Cloud Outsourcing  
**Document Reference:** ZDB-LLM-ARCH-D1-001  
**Status:** Approved for Implementation  

---

## 1. Executive Summary

Zarya Digital Bank currently faces a critical customer support bottleneck. Customers communicate primarily in **UrduLish** (e.g., *"Mera Raast transfer fail ho gaya lekin paise kat gaye"*, *"Debit card block karna hai, gum ho gaya hai"*). Initial trials using third-party commercial APIs (such as OpenAI GPT-4) revealed three fatal shortcomings:
1. **Regulatory Non-Compliance & Privacy:** SBP data sovereignty regulations strictly prohibit exporting personally identifiable customer financial queries to external foreign servers.
2. **Prohibitive Cost at Scale:** Processing ~50,000 conversations daily (averaging 800 tokens per dialogue) costs upwards of \$30,000–\$50,000 monthly in API tokens.
3. **Tone and Behavioral Mismatch:** Generic public models hallucinate Pakistani banking regulations, sound overly robotic in UrduLish, fail to recognize local slang/typos, and risk leaking sensitive OTP/PIN instructions.

To establish an autonomous, secure, and accurate AI banking assistant, we evaluated four architectural paradigms:
- **Approach 1:** Prompt Engineering Only (Commercial API)
- **Approach 2:** Retrieval-Augmented Generation (RAG) Only (Commercial or Base Model)
- **Approach 3:** Supervised Fine-Tuning (SFT) Only (Self-Hosted Open Weights Model)
- **Approach 4:** **Hybrid: Fine-Tuned Domain LLM + Local Policy RAG (Selected)**

This document provides the technical, financial, and operational justification for selecting the **Fine-Tuning + RAG Hybrid Architecture**.

---

## 2. Comparative Evaluation Matrix

| Evaluation Criteria | 1. Prompt Engineering Only | 2. RAG Only (Base Model) | 3. Fine-Tuning Only (SFT) | 4. Fine-Tuning + RAG Hybrid (Selected) |
| :--- | :--- | :--- | :--- | :--- |
| **Quality & Tone (UrduLish)** | **Poor to Moderate:** Sounds stiff, translates idioms literally, struggles with colloquial Pakistani phonetic spelling. | **Moderate:** Retrieves accurate English/Urdu facts, but base model fails to synthesize natural, empathetic UrduLish. | **Very High:** Internalizes natural banking UrduLish, regional greetings (*"Ji Janab"*, *"Ma'azrat chahte hain"*), and concise style. | **Superior:** Native UrduLish fluency, polite banking persona, coupled with zero-hallucination factual precision. |
| **Factual Adherence & Updates** | **Poor:** Base models invent transaction limits, turnaround times (TAT), and fee structures from pretraining memory. | **High:** Facts grounded in retrieved chunks, but base models struggle to parse mixed-language policy documents correctly. | **Fragile:** Model parameters bake in facts. Whenever fee schedules or Raast limits change, expensive retraining is needed. | **Dynamic & Flawless:** Retrieval layer injects live Schedule of Charges (SOC), transaction limits, and circulars instantly without retraining. |
| **Customer Data Privacy** | **Non-Compliant:** Sends full user queries, account summaries, and metadata to third-party offshore cloud APIs. | **Non-Compliant (if API-based):** External API egress violates SBP Data Sovereignty Circulars. | **Fully Compliant:** Runs 100% on-premises or inside the bank's secure private cloud VPC. | **Fully Compliant:** Air-gapped / private VPC deployment. Vector store and LLM inference reside inside the bank's security perimeter. |
| **Inference Latency (p95)** | **High (1,500 – 3,500 ms):** External network roundtrips, large system prompt overhead, public API queueing. | **High (2,000 – 4,500 ms):** Embedding generation + vector search + long augmented context window = high latency. | **Ultra-Low (250 – 500 ms):** Compact prompt, quantized 4-bit / 8-bit model served with vLLM / continuous batching. | **Low (400 – 900 ms):** Fast local vector search (dense/sparse) + compact domain prompt + optimized vLLM serving. |
| **Operational Cost (50k msgs/day)** | **Extremely High:** \$35,000 – \$50,000 / month in recurring token charges with zero asset equity. | **High to Moderate:** \$20,000 – \$35,000 / month API costs plus external vector index fees. | **Low:** Fixed hardware amortisation (\$1,500/month GPU node or on-prem cluster). \$0 incremental token cost. | **Optimal:** Fixed infrastructure cost (\$1,500 – \$2,200/month for dedicated GPU/vLLM + PostgreSQL pgvector). High ROI. |
| **Structured Output Reliability** | **Moderate (80–88%):** Requires heavy prompt engineering; frequent JSON markdown fence syntax errors. | **Moderate (82–90%):** Context pollution degrades structured schema generation consistency. | **High (95–98%):** Weights are conditioned on exact JSON schema targets for tickets and intent classification. | **Near Perfect (99%+):** Fine-tuned for exact JSON schema; constrained decoding (outlines/vLLM) guarantees valid parsing. |
| **Safety & Anti-Fraud Reflex** | **Vulnerable:** Prone to system prompt injection, jailbreaks, and indirect prompt extraction. | **Vulnerable:** Adversarial customer prompts can override prompt instructions and leak credentials. | **Robust:** Refusal behavior is deep-seated in model weights; instinctively refuses OTP/PIN inquiries. | **Defense-in-Depth:** Weight-level safety alignment (SFT + DPO) reinforced by deterministic pre-inference guardrail filters. |
| **Engineering Effort** | **Minimal:** 1–2 weeks to write and tweak prompts. | **Moderate:** 3–4 weeks for chunking, embedding, vector DB, and reranking pipelines. | **High:** 4–6 weeks for dataset synthesis, LoRA/QLoRA training, and evaluation harness. | **High Initial Investment:** 6–8 weeks for end-to-end dataset, fine-tuning, RAG integration, and guardrails. |

---

## 3. In-Depth Architectural Analysis

### 3.1 Why "Prompt Engineering Only" Fails Zarya Digital Bank
1. **Regulatory Violation (SBP BPRD):** Under State Bank of Pakistan governance, customer financial transaction inquiries cannot leave domestic borders. Sending real-time transaction dispute queries containing customer mobile numbers, dispute amounts, and transaction IDs to foreign LLM APIs constitutes an immediate compliance breach.
2. **Context Window Tax & Cost Bloat:** To force a base model to speak fluent banking UrduLish and obey 50+ banking policies, the system prompt must exceed 2,500 tokens per request. At 50,000 queries/day:
   $$\text{Daily Input Tokens} = 50,000 \times 3,000 = 150,000,000 \text{ tokens/day}$$
   $$\text{Monthly Cost} \approx \$36,000 \text{ to } \$54,000 \text{ USD / month}$$
   This is economically unsustainable for retail customer support.
3. **Phonetic & Dialectal Fragility:** Base commercial models have seen minuscule Roman Urdu corpus in pretraining. Words like *"kat"* (deducted), *"phansa"* (stuck), *"chori"* (theft), *"nhi chal rha"* (not working), and *"raast id"* confuse the model into giving robotic Hindi or bizarre English translations.

### 3.2 Why "RAG Only" Is Insufficient
1. **Style Cannot Be Retrieved:** RAG retrieves knowledge chunks (e.g., *"Raast Transaction Limit: PKR 200,000 per day"*). It does **not** teach the model empathy, concise phrasing, or culturally resonant de-escalation for an agitated Pakistani customer whose salary transfer failed.
2. **Query Reformulation Failure in Roman Urdu:** A customer writes: *"bhai mera paisa cut gya raast se lkn samne wale ko ni mila 2 din hogye kya scene h"*. Base embedding models (OpenAI `text-embedding-3-small`, standard BERT) fail to link this query to the official English policy document titled *"Raast Dispute Resolution & Settlement Turnaround Times"*.
3. **High Latency Overhead:** Passing 4–5 retrieved paragraphs into every prompt slows down Time-to-First-Token (TTFT) to over 2.5 seconds, frustrating users on mobile 4G/3G connections.

### 3.3 Why "Fine-Tuning Only" Is Dangerous for Banking
1. **Knowledge Decay & Catastrophic Parametric Hallucination:** Banking policies are volatile. The State Bank frequently updates Raast transaction limits, ATM withdrawal taxes, international e-commerce FED (Federal Excise Duty), and savings account profit rates. 
2. If banking facts are baked purely into model weights:
   - When the bank reduces ATM fees from PKR 23.44 to PKR 18.75, the fine-tuned model will continue quoting PKR 23.44.
   - Retraining and redeploying a 3B/7B model weekly just to update 3 policy numbers is operationally reckless and cost-inefficient.

---

## 4. The Solution: The Fine-Tuning + RAG Hybrid Architecture

The hybrid paradigm cleanly decouples **Behavior & Language** from **Dynamic Facts**:

```
+-----------------------------------------------------------------------------------+
|                           ZARYA HYBRID ARCHITECTURE                               |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|   1. FINE-TUNING (The "Brain & Voice"):                                           |
|      - Teaches the model HOW to speak: Natural UrduLish, Roman Urdu, English.    |
|      - Enforces Bank Persona: Courteous ("Ji", "Aap"), concise, calming.          |
|      - Internalizes Safety & Hard Boundaries: 100% refusal to ask for OTP/PIN.   |
|      - Enforces Structured Output: Zero-shot schema compliance for ticket JSON.   |
|                                                                                   |
|   2. RAG (The "Memory & Reference Library"):                                     |
|      - Injects WHAT to know: Live Schedule of Charges (SOC), interest rates.     |
|      - Grounded in official ZDB SOPs, Turnaround Times (TAT), SBP circulars.      |
|      - Updates instantaneously by re-indexing markdown/PDF files (0 retraining). |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

### Concrete Architectural Flow:
1. **Customer Inbound Message:** Customer types in UrduLish on Mobile App or WhatsApp.
2. **Local Guardrails (Pre-Filter):** Presidio regex masks any customer-typed CNIC or full card numbers; prompt injection detector screens adversarial inputs.
3. **Intent Classification & RAG Routing:**
   - If the intent requires dynamic facts (e.g., fee schedules, international card transaction limits, savings interest rates), the system retrieves the top-2 verified policy chunks using a multilingual embedding model (`multilingual-e5-base` or `BGE-M3`).
   - If the intent is conversational, safety-critical, or pure ticket creation (e.g., lost card block, OTP scam warning), RAG is bypassed to ensure sub-300ms latency.
4. **Fine-Tuned Small LLM (Qwen 2.5 3B / Llama 3.2 3B Q4_K_M):**
   - The fine-tuned model ingests the query (and concise retrieved snippet if applicable).
   - Generates immediate, empathetic, fluent UrduLish advice.
   - Emits structured JSON containing ticket category, urgency, and Turnaround Time (TAT) for the core banking system.

---

## 5. Economic & Technical Justification for Zarya Digital Bank

### 5.1 Total Cost of Ownership (TCO) Breakdown (50,000 queries/day)

| Cost Component | Approach 1: Commercial API (GPT-4o mini / Claude) | Approach 4: Hybrid Fine-Tuned Model (vLLM on 1x RTX 4090 / A10G) |
| :--- | :--- | :--- |
| **API Token Cost** | \$0.15/1M in + \$0.60/1M out + heavy prompt $\approx$ **\$2,250 – \$3,600 / month** | **\$0.00** (Zero token charges) |
| **Data Privacy Penalty Risk** | SBP Non-compliance fines: Up to PKR 50,000,000 + operational sanction risk | **\$0.00** (100% on-premises data residency) |
| **Compute / Server Hosting** | Zero hosting (SaaS) | 1x Cloud/Dedicated GPU instance (RunPod/Hetzer/On-prem) $\approx$ **\$350 – \$650 / month** |
| **Vector DB / Storage** | External SaaS Vector DB: **\$250 / month** | Self-hosted PostgreSQL with `pgvector`: **\$50 / month** |
| **Annualized Total Run Cost** | **\$32,000 – \$48,000 / year** | **\$4,800 – \$8,400 / year** |
| **Net Savings** | Baseline | **> 78% Annual Cost Reduction ($25k - $40k/yr saved)** |

### 5.2 Latency and Customer Experience
- **Commercial API:** Average round-trip latency across Pakistani ISP networks to US/EU cloud regions is **1,800ms – 3,200ms**.
- **Self-Hosted Quantized Model (Q4_K_M on vLLM):** P50 latency is **280ms**, P95 latency is **720ms**. Immediate response in WhatsApp and mobile banking UI prevents user drop-off.

---

## 6. Implementation Recommendation & Roadmap

1. **Day 1 Focus (Dataset Engineering):** Build a 3,000+ example synthetic dataset rigorously balancing UrduLish conversational queries, multi-turn dispute resolutions, strict OTP/PIN safety refusals, and structured JSON ticketing outputs.
2. **Day 2 Focus (SFT with LoRA/QLoRA):** Fine-tune candidate 3B open-weight models (Qwen 2.5 3B / Llama 3.2 3B) using parameter-efficient QLoRA.
3. **Day 3 Focus (DPO Alignment):** Direct Preference Optimization against human rejection criteria (polite vs. robotic, secure vs. over-compliant).
4. **Day 4 Focus (Quantization & Hybrid RAG):** Quantize to 4-bit GGUF / AWQ, wire local vector store over Zarya's Schedule of Charges, and integrate Presidio PII guardrails.
5. **Day 5 Focus (Production Serving & Handover):** Deploy containerized FastAPI + vLLM stack with support agent escalation ticketing.

**Conclusion:** The Fine-Tuning + RAG Hybrid is not merely an alternative; it is the **only architecture** that simultaneously satisfies the State Bank of Pakistan's privacy regulations, guarantees low-cost scalability at 50,000 daily messages, and delivers authentic, empathetic UrduLish customer interactions.
