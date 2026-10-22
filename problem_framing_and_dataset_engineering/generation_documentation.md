# Synthetic Data Generation & Cost Documentation

**Client:** Zarya Digital Bank (Fictional Pakistani Digital Retail Bank)  
**Task:** Task 3 — Synthetic Data Generation & Expansion Pipeline  
**Target:** $\ge$ 3,000 High-Quality Training Examples (Achieved: 3,200 raw examples)  
**Document Reference:** ZDB-SYNTH-DOC-001  

---

## 1. Generation Pipeline Architecture

To create an authentic, resilient dataset that prepares a small model (3B parameters) to outperform commercial generic models on local Pakistani banking queries, we engineered a multi-stage synthetic expansion pipeline:

```
+---------------------------------------------------------------------------------------+
|                       SYNTHETIC DATA GENERATION PIPELINE                              |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|   [100+ Hand-Crafted Canonical Seeds]                                                 |
|   (seed_data.py: Raast, IBFT, ATM failures, Lost cards, Scam calls, SBP rules)       |
|                                     │                                                 |
|                                     ▼                                                 |
|   [Persona & Dialectal Injector]                                                      |
|   ├── Polite Salaried Employee  (Formal Roman Urdu, respectful)                       |
|   ├── Panicked Merchant         (Urgent cash flow, short anxious sentences)           |
|   ├── Gen-Z Student             (Heavy English-Urdu code switching, slang)            |
|   ├── Elderly Pensioner         (Confused, vulnerable to social engineering)          |
|   └── Angry / Frustrated User   (Threats of State Bank escalation, shouting)          |
|                                     │                                                 |
|                                     ▼                                                 |
|   [Phonetic Variation & Noise Layer]                                                  |
|   ├── Phonetic Roman Urdu variants ("paise" -> "pesy", "nahi" -> "nhi", "karo")      |
|   └── Slang / Abbreviations ("plz", "asap", "bro", "lkn", "bht")                      |
|                                     │                                                 |
|                                     ▼                                                 |
|   [Task Mix & Quota Allocator]                                                        |
|   ├── Multi-Turn Dialogues (>= 20% quota -> 750 examples generated = 23.4%)          |
|   ├── Structured Output JSON (>= 300 quota -> 480 examples generated)                 |
|   ├── Safety & Fraud Refusals (>= 300 quota -> 904 examples generated)                |
|   └── General Banking FAQs & Inquiries (~1,066 examples)                              |
|                                     │                                                 |
|                                     ▼                                                 |
|   [Raw Dataset Output] ➔ 3,200 Balanced Records in data/raw_dataset.jsonl             |
+---------------------------------------------------------------------------------------+
```

---

## 2. Teacher LLM Prompts & Metaprompts

During pipeline bootstrapping, Teacher LLMs (such as Claude 3.5 Sonnet and GPT-4o) were prompted to expand canonical scenarios into conversational turns, while enforcing banking policies and Pakistani linguistic nuances.

### 2.1 Metaprompt 1: Conversational Expansion (Multi-Turn & Urgency)

```text
SYSTEM PROMPT:
You are an expert Pakistani banking prompt engineer and computational linguist.
Your goal is to generate realistic training dialogues between a Pakistani retail bank customer and Zarya Digital Bank's AI customer support assistant.

RULES:
1. CUSTOMER INPUT:
   - Must be written in natural UrduLish (Roman Urdu mixed with English banking words).
   - Reflect natural human typing habits: occasional typos ("nhi", "gya", "pesy", "plz"), emotional urgency, or slang.
   - Embody one of 5 customer personas: [Polite Salaried, Panicked Merchant, Gen-Z Student, Elderly User, Frustrated Customer].
   - Vary turn lengths from short frantic cries ("pese kat gye!") to detailed problem descriptions.

2. ASSISTANT OUTPUT:
   - Tone: Courteous ("Ji", "Aap", "Janab"), empathetic, calming, and concise (2-4 sentences max).
   - Strictly follow State Bank of Pakistan (SBP) regulatory turnaround times (TAT):
     * Raast transfer dispute: 24 hours.
     * IBFT interbank dispute: 24-48 working hours.
     * Own-bank ATM dispute: 48 hours; Other-bank ATM dispute: 7-10 working days.
     * Card delivery: 3-5 business days.
   - NEVER ask for OTP, PIN, password, CVV, or full card number.

3. CONVERSATION FORMAT:
   Emit as a valid JSON object with role ("system", "user", "assistant") and content.
```

### 2.2 Metaprompt 2: Structured JSON Ticket Generation

```text
SYSTEM PROMPT:
You are Zarya Bank's automated triage engine. Given the customer query, classify their intent, assess urgency, determine if a ticket is required, and output a valid JSON response adhering strictly to the provided Pydantic schema:

{
  "intent": "<string>",
  "category": "transfers_payments" | "cards_atm" | "account_balance" | "loans_products" | "complaints_disputes" | "fraud_security" | "out_of_scope",
  "sub_category": "<string>",
  "urgency": "low" | "medium" | "high" | "critical",
  "sentiment": "positive" | "neutral" | "anxious" | "worried" | "frustrated" | "angry" | "panicked",
  "requires_ticket": true | false,
  "ticket_details": {
    "ticket_id": "ZDB-XXXXXXXX",
    "priority": "P1" | "P2" | "P3" | "P4",
    "estimated_tat_hours": <int>,
    "action_needed": "<string>",
    "summary_english": "<string>"
  } | null,
  "customer_response_urdulish": "<string>"
}

CRITICAL: Output ONLY valid raw JSON. No introductory pleasantries, no markdown triple backticks.
```

---

## 3. Token Economics & Generation Cost Analysis

The cost to generate, synthesize, and filter the complete 3,200 dataset using commercial Teacher LLMs is modeled below based on current enterprise pricing (October 2024 / 2026 standard rates):

### 3.1 Token Consumption Breakdown per Sample

| Conversation Type | Sample Count | Avg. Input Tokens (Prompt + Few-Shot) | Avg. Output Tokens (Completion) | Total Input Tokens | Total Output Tokens |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Standard Single-Turn** | 1,970 | 650 | 180 | 1,280,500 | 354,600 |
| **Multi-Turn (2–4 turns)** | 750 | 950 | 380 | 712,500 | 285,000 |
| **Structured JSON Tickets**| 480 | 800 | 260 | 384,000 | 124,800 |
| **Total Generation Volume**| **3,200** | — | — | **2,377,000 tokens** | **764,400 tokens** |

### 3.2 Teacher LLM Pricing Comparison

| Provider / Model | Input Price / 1M Tokens | Output Price / 1M Tokens | Total Cost for 3,200 Dataset |
| :--- | :--- | :--- | :--- |
| **OpenAI GPT-4o** | \$2.50 | \$10.00 | $(2.377 \times 2.50) + (0.764 \times 10.00) = \$5.94 + \$7.64 = $ **\$13.58** |
| **OpenAI GPT-4o-mini** | \$0.15 | \$0.60 | $(2.377 \times 0.15) + (0.764 \times 0.60) = \$0.36 + \$0.46 = $ **\$0.82** |
| **Anthropic Claude 3.5 Sonnet** | \$3.00 | \$15.00 | $(2.377 \times 3.00) + (0.764 \times 15.00) = \$7.13 + \$11.46 = $ **\$18.59** |
| **Google Gemini 1.5 Flash** | \$0.075 | \$0.30 | $(2.377 \times 0.075) + (0.764 \times 0.30) = \$0.18 + \$0.23 = $ **\$0.41** |
| **Local Deterministic Generator** | **\$0.00** | **\$0.00** | **\$0.00 (Zero API Expense)** |

### 3.3 Production Recommendation:
For iterative dataset bootstrapping, running a hybrid approach using **Gemini 1.5 Flash / GPT-4o mini** for expansion seed review at under **\$1.00 USD** total cost, combined with deterministic rule-based syntactic variation, provides the optimum balance of enterprise quality, dialectal fidelity, and zero budget waste.
