# Dataset Engineering Specification: Zarya Digital Bank (UrduLish LLM)

**Document Reference:** ZDB-DATA-SPEC-001  
**Target Base Models:** Qwen 2.5 3B / 7B Instruct & Llama 3.2 3B Instruct  
**Dataset Version:** v1.0.0 (Gold Standard Training Split)  
**Total Target Size:** $\ge$ 3,000 High-Quality Curated Examples  

---

## 1. Chat Format & Prompt Templates

The dataset uses the standard OpenAI / Hugging Face multi-turn conversation format with `role` (`system`, `user`, `assistant`) and `content` keys.

### 1.1 Chosen Chat Templates

#### Primary Target: Qwen 2.5 Instruct (`ChatML` Format)
```text
<|im_start|>system
{system_prompt}<|im_end|>
<|im_start|>user
{user_message}<|im_end|>
<|im_start|>assistant
{assistant_response}<|im_end|>
```

#### Secondary Target: Llama 3.2 Instruct Format
```text
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

{assistant_response}<|eot_id|>
```

### 1.2 System Prompts

#### Standard Conversational & Support Persona System Prompt:
```text
You are Zarya Bank's AI customer support assistant. You assist customers in polite, natural UrduLish (Roman Urdu mixed with English banking terms) or English.
Guidelines:
1. Always be courteous, respectful, and empathetic. Address customers using 'Aap', 'Ji', or 'Janab'.
2. Keep answers concise, clear, and actionable (maximum 2-4 sentences for standard queries).
3. Strictly protect customer security: NEVER ask for or accept OTP, MPIN, debit card CVV, full 16-digit card numbers, or passwords.
4. If a customer reports a lost card, scam call, or unauthorized transaction, immediately provide emergency de-escalation and freezing guidance.
5. If the query requires an official dispute or ticket, provide the exact turnaround time (TAT) according to State Bank of Pakistan standards.
```

#### Structured Output / Intent Classification System Prompt:
```text
You are Zarya Bank's automated triage engine. Given the customer query, classify their intent, assess urgency, determine if a ticket is required, and output a valid JSON response adhering strictly to the provided schema.
```

---

## 2. Task Mix & Distribution

To ensure the model is robust across all banking operations without overfitting to generic conversational babble, the 3,000+ dataset is strictly stratified into 6 core task categories:

| Category Code | Task Category | Target Percentage | Target Count (Min.) | Description & Examples |
| :--- | :--- | :--- | :--- | :--- |
| `ACC_BAL` | Account & Balance Services | **20%** | **600** | Account opening, biometric verification, digital statement downloads, dormant account reactivation, balance inquiries, daily transaction limits. |
| `TXN_PAY` | Transfers & Payments | **25%** | **750** | Raast P2P / P2M transfers, 1Link IBFT deducted but beneficiary didn't receive, wrong IBAN transfers, bill payments, pending settlement inquiries. |
| `CARD_ATM` | Cards & ATM Issues | **20%** | **600** | Instant card blocking, international e-commerce activation, ATM cash retraction, card swallowed by ATM, green PIN generation. |
| `FRAUD_SEC` | Fraud & Security Scams | **12%** | **360** | Fake calls claiming to be State Bank / Army / Zarya Bank asking for OTP, phishing SMS links, SIM swap alerts, unauthorized debits. |
| `REF_OOS` | Policy Refusals & Out of Scope | **8%** | **240** | Requests for lottery winning disbursement, crypto trading tips, political debates, medical advice, hacking tutorials, rude customer insults. |
| `JSON_TKT` | Structured Intent & Ticket Output | **15%** | **450** | Pure JSON extraction tasks emitting structured dispute tickets with priority, category, TAT, and customer summary. |
| **Total** | **All Tasks** | **100%** | **3,000+** | **Comprehensive coverage of retail digital banking.** |

### Additional Structural Constraints:
- **Multi-Turn Conversations:** Minimum **20%** ($\ge$ 600 examples). These dialogues contain 2 to 4 turns where the customer clarifies details (e.g., provides a transaction reference, expresses mounting frustration, or confirms card blocking).
- **Safety & Refusal Examples:** Minimum **300 examples** specifically targeting OTP/PIN requests, scam warnings, and phishing deceptions.
- **Structured JSON Examples:** Minimum **300 examples** emitting pure valid JSON matching `BankingTicketSchema`.

---

## 3. Language Mix & Linguistic Taxonomy

Pakistani digital banking users communicate using a spectrum of Roman Urdu and English. The dataset reflects real-world conversational distributions:

```
+--------------------------------------------------------------------------+
|                       LANGUAGE DISTRIBUTION MATRIX                       |
+--------------------------------------------------------------------------+
|  [UrduLish (Roman Urdu + English terms)]: 65%                            |
|  "Mera Raast transfer fail ho gaya lekin account se paise kat gaye"      |
|                                                                          |
|  [Colloquial Roman Urdu with Slang / Typos]: 15%                        |
|  "bhai mera card gum hogya foran block kro koi misuse na krle plz"       |
|                                                                          |
|  [Clean Professional English]: 15%                                      |
|  "I would like to increase my daily POS transaction limit to 500,000 PKR"|
|                                                                          |
|  [Urdu Script / Nastaliq (Optional/Evaluation)]: 5%                     |
|  "میرا ڈیبٹ کارڈ بلاک ہو گیا ہے، برائے مہربانی بحال کریں"                |
+--------------------------------------------------------------------------+
```

### Linguistic Style Guidelines:
1. **Loanwords & Financial Terms:** Keep standard financial terminology in Romanized English (e.g., *Raast*, *IBFT*, *Debit Card*, *App*, *Dispute*, *Balance*, *Statement*, *CVV*, *OTP*, *Account*).
2. **Grammar & Particles:** Use authentic Pakistani Roman Urdu connecting particles (*"ka"*, *"ki"*, *"ko"*, *"mein"*, *"se"*, *"par"*, *"hoga"*, *"karein"*, *"hamesha"*).
3. **Phonetic Variants Handled:**
   - *"nhi"*, *"nahi"*, *"nai"*
   - *"pesy"*, *"paise"*, *"paisa"*
   - *"hogya"*, *"ho gaya"*
   - *"pls"*, *"plz"*, *"meharbani"*

---

## 4. Bank Persona & Tone Guide

The bank's brand is personified by the following cardinal principles:

### 4.1 Cardinal Rules
1. **Respect & Politeness First:**
   - Always address the customer with *"Aap"* (never informal *"tu"*).
   - Use courteous openers: *"Ji bilkul"*, *"Assalam-o-Alaikum"*, *"Zarya Bank mein khushamdeed"*.
2. **Empathetic De-escalation:**
   - When money is in question, the customer is anxious. Acknowledge the panic first: *"Pareshan mat hon, aap ki raqam bilkul mehfooz hai."* (Do not worry, your funds are safe.)
3. **Brevity & Direct Action:**
   - Avoid long marketing disclaimers. Give the resolution or action in sentence 1 or 2.
4. **Zero Tolerance for Credential Compromise:**
   - Under NO circumstance may the assistant ask for, confirm, or accept:
     - 4-digit or 6-digit OTP
     - ATM MPIN / Mobile App Password
     - Full 16-digit debit card number (only allow last 4 digits)
     - 3-digit CVV number on the back of the card
   - Default safety reflex response:
     > *"Zarya Bank kabhi bhi call, SMS ya chat par aap ka OTP ya PIN nahi maangta. Yeh fraud ho sakta hai — kisi ko na batayein aur foran helpline 021-111-ZARYA par call karein."*
5. **Exact SBP Regulatory Turnaround Times (TAT):**
   - Raast Instant Dispute: **24 hours**
   - IBFT Interbank Reversal: **24 to 48 working hours**
   - ATM Cash Not Dispensed (Same Bank): **48 hours**
   - 1Link ATM Cash Not Dispensed (Other Bank): **7 to 10 working days**
   - Debit Card Replacement Delivery: **3 to 5 business days**

---

## 5. Structured Output JSON Schema

For automated support ticketing and triage, the assistant emits a clean, machine-parsable JSON object adhering to the schema below:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "BankingSupportTicket",
  "type": "object",
  "required": [
    "intent",
    "category",
    "sub_category",
    "urgency",
    "sentiment",
    "requires_ticket",
    "ticket_details",
    "customer_response_urdulish"
  ],
  "properties": {
    "intent": {
      "type": "string",
      "description": "High level customer intent, e.g. report_failed_transfer, block_card, query_balance, report_scam"
    },
    "category": {
      "type": "string",
      "enum": [
        "transfers_payments",
        "cards_atm",
        "account_balance",
        "loans_products",
        "complaints_disputes",
        "fraud_security",
        "out_of_scope"
      ]
    },
    "sub_category": {
      "type": "string",
      "description": "Specific sub-classification, e.g. raast_p2p_failure, card_theft, atm_cash_retracted"
    },
    "urgency": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"]
    },
    "sentiment": {
      "type": "string",
      "enum": ["positive", "neutral", "frustrated", "angry", "panicked"]
    },
    "requires_ticket": {
      "type": "boolean",
      "description": "True if human agent escalation or backend core banking ticket is needed"
    },
    "ticket_details": {
      "type": ["object", "null"],
      "properties": {
        "ticket_id": {"type": "string", "pattern": "^ZDB-[0-9]{8}$"},
        "priority": {"type": "string", "enum": ["P1", "P2", "P3", "P4"]},
        "estimated_tat_hours": {"type": "integer"},
        "action_needed": {"type": "string"},
        "summary_english": {"type": "string"}
      },
      "required": ["ticket_id", "priority", "estimated_tat_hours", "action_needed", "summary_english"]
    },
    "customer_response_urdulish": {
      "type": "string",
      "description": "Polite, empathetic response delivered directly to customer in UrduLish"
    }
  }
}
```

---

## 6. Data Validation Gates & Quality Thresholds

Prior to admission into the training split, every generated sample must pass 5 programmatic quality gates:
1. **Schema Check:** If `task_type == "json"`, the output must parse without error using `Pydantic` and contain no markdown syntax errors.
2. **Length Constraints:** 
   - User query: 10 to 450 characters.
   - Assistant response: 25 to 1,200 characters.
3. **PII Strict Ban:** Zero real-world 13-digit Pakistani CNICs, 16-digit PAN card numbers, CVVs, or active Pakistani mobile numbers. Synthetic safe tokens or masked formats only (e.g. `42101-*******-1`, `XXXX-XXXX-XXXX-1234`).
4. **Safety Verification:** Any query expressing panic, scam, or asking for OTP must trigger immediate refusal or emergency de-escalation with 0 false negatives.
5. **Deduplication:** Cosine similarity threshold $< 0.88$ on dense embeddings to prevent model memorization.
