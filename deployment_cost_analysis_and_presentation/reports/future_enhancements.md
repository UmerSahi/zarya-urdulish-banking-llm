# Strategic Roadmap & Future Enhancements

**Client:** Zarya Digital Bank (Pakistan)  
**Task:** Week 10 Capstone — Day 5 Task 5  
**Time Horizon:** 6 to 18 Months Post-Deployment  

---

## 1. Executive Vision

Having successfully proven that an open-source, fine-tuned 3B model outperforms commercial foreign APIs on UrduLish fluency, response speed, regulatory safety, and cost, Zarya Digital Bank is positioned to lead Pakistani fintech in sovereign AI adoption.

The roadmap outlines four core evolution phases:
```
[Phase 1: Multilingual & Voice] ──► [Phase 2: Mobile On-Device Edge] ──► [Phase 3: Core API Tool Calling] ──► [Phase 4: Real-Time Fraud RAG]
```

---

## 2. Roadmap Phases & Detailed Initiatives

### Phase 1: Native Urdu Script & Voice Banking Assistant (Months 1–4)
* **Urdu Nastaliq Script Support:**
  * While Roman Urdu / UrduLish serves app users, rural banking and WhatsApp demographics heavily utilize Nastaliq Urdu (`اردو`).
  * Extend tokenizer and SFT training with 5,000 Nastaliq banking dialogues.
* **Whisper Speech-to-Text (STT) & Piper TTS:**
  * Implement local, sovereign audio inference so users can speak their complaints via WhatsApp voice notes.

### Phase 2: Mobile Edge Distillation for Offline / Zero-Latency Support (Months 4–8)
* **Knowledge Distillation into 1.5B / 0.5B Architectures:**
  * Distill teacher knowledge from Qwen 2.5 3B into **Qwen 2.5 1.5B** or **1B mobile-friendly models**.
* **On-Device CoreML / TFLite Quantization:**
  * Run offline FAQ and balance queries directly inside iOS and Android apps without cellular data consumption.

### Phase 3: Function Calling & Core Banking API Integration (Months 8–12)
* **Direct Integration with Core Banking Switches (Temenos / Flexcube / 1Link):**
  * Train structured function-calling tokens allowing the LLM to execute authenticated customer actions:
    - `fetch_account_balance(account_token)`
    - `freeze_debit_card(card_last_4, auth_token)`
    - `trace_1link_rrn(rrn_code)`
* **Strict Two-Factor Authentication (2FA) Tool Gating:**
  * Autonomous fund movements or card blocks will prompt an in-app biometric/FaceID biometric confirmation challenge.

### Phase 4: Regional Language Expansion & Multi-Tenant Fraud Graph (Months 12–18)
* **Regional Language Support:**
  * Expand fine-tuning to major Pakistani regional languages: **Pashto, Punjabi, and Sindhi**.
* **GraphRAG & Cross-Session Fraud Detection:**
  * Couple the LLM with a Neo4j Graph Database to spot coordinated social engineering rings (e.g. multiple distinct customers reporting fraudulent calls from the identical unregistered SIM or jazzcash number).

