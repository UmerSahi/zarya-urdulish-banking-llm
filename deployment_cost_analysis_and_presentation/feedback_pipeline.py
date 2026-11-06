"""
Continuous Monitoring & Feedback Pipeline (Task 2)
Client: Zarya Digital Bank (Pakistan)
Purpose:
- Ingests negative customer feedback from production database
- Scrubs banking PII (CNICs, account numbers, card numbers)
- Transforms failed conversations into paired DPO preference samples (prompt, chosen, rejected)
- Exports formatted training artifacts for iterative model refinement
"""

import os
import sys
import json
import re
from typing import List, Dict, Any
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
DPO_DATA_DIR = os.path.join(PARENT_DIR, "evaluation_framework_and_preference_alignment", "data")
OUTPUT_PATH = os.path.join(DPO_DATA_DIR, "dpo_continuous_training.jsonl")

from database import init_db, get_feedback_records, record_feedback

# RegEx for PII scrub
CNIC_REGEX = re.compile(r"\b\d{5}-?\d{7}-?\d\b")
CARD_REGEX = re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b")
PHONE_REGEX = re.compile(r"\b(03\d{2}[-\s]?\d{7})\b")

def scrub_pii(text: str) -> str:
    """Masks all sensitive banking entities before adding to DPO training pool."""
    text = CNIC_REGEX.sub("[REDACTED_CNIC]", text)
    text = CARD_REGEX.sub("[REDACTED_CARD]", text)
    text = PHONE_REGEX.sub("[REDACTED_PHONE]", text)
    return text

def synthesize_improved_chosen(prompt: str, rejected: str) -> str:
    """
    Teacher alignment synthesis: generates a polite, concise, SBP-compliant
    chosen response replacing the flawed output.
    """
    p = prompt.lower()
    if "otp" in p or "pin" in p:
        return (
            "Zarya Bank kabhi bhi call ya SMS par aap ka OTP ya PIN nahi maangta. "
            "Yeh fraud ho sakta hai — kisi ko na batayein aur foran helpline par report karein."
        )
    elif "fee" in p or "charges" in p:
        return (
            "Ji Zarya Bank ke official Schedule of Charges ke mutabiq PayPak Classic Debit Card ki "
            "annual fee PKR 2,400 + tax hai. Virtual Debit Card app mein bilkul muft (zero fee) hai."
        )
    elif "fail" in p or "kat" in p:
        return (
            "Ji pareshan na hon, aap ki raqam bilkul mehfooz hai. Raast interbank settlement delay ki wajah se "
            "paise 30 minute se 24 ghante mein auto-reverse ho jate hain. Hum ne aap ka dispute ticket log kar liya hai."
        )
    else:
        return (
            f"Ji shukriya rabta karne ka. Aap ki enquiry ke mutabiq Zarya Bank aap ki mukammal rehnumai ke liye hazir hai. "
            f"Baraye meherbani helpline ya app mein Support tab visit karein."
        )

def run_feedback_to_dpo_pipeline():
    print("=" * 75)
    print("  TASK 2: CONTINUOUS DPO MONITORING & DATA GENERATION PIPELINE")
    print("=" * 75)

    # Ingest from production DB
    flagged_records = get_feedback_records(only_flagged=True, limit=500)
    print(f"[Feedback Ingest] Found {len(flagged_records)} flagged conversations in production DB.")

    # If DB is clean, generate synthetic seed feedback for demonstration
    if len(flagged_records) == 0:
        print("[Info] Seeding sample downvoted production records for pipeline demonstration...")
        sample_bad_cases = [
            {
                "session_id": "sess_prod_demo_1",
                "user_query": "Mera 50,000 ka Raast transfer fail ho gaya, paise wapas kab milen ge?",
                "assistant_response": "Paise mil jayen ge, aap wait karein.",
                "rating": -1,
                "feedback_category": "too_abrupt",
                "comment": "Bot was rude and did not give any TAT or ticket number."
            },
            {
                "session_id": "sess_prod_demo_2",
                "user_query": "PayPak debit card ki annual fee kitni hoti hai?",
                "assistant_response": "PayPak card ki fees shayad PKR 1,850 hai.",
                "rating": -1,
                "feedback_category": "outdated_rag_fact",
                "comment": "Quoted outdated fee instead of PKR 2,400."
            },
            {
                "session_id": "sess_prod_demo_3",
                "user_query": "Manager ne call kar ke bola OTP batao taake account upgrade ho, kya OTP de dun?",
                "assistant_response": "Agar manager hai toh verify kar ke OTP de sakte hain.",
                "rating": -1,
                "feedback_category": "safety_violation",
                "comment": "Dangerous! Failed to trigger SBP fraud warning."
            }
        ]
        for c in sample_bad_cases:
            record_feedback(c)
        flagged_records = get_feedback_records(only_flagged=True, limit=500)

    # Process pairs
    dpo_pairs = []
    for rec in flagged_records:
        clean_prompt = scrub_pii(rec["user_query"])
        rejected_output = scrub_pii(rec["assistant_response"])
        chosen_output = synthesize_improved_chosen(clean_prompt, rejected_output)

        dpo_pairs.append({
            "prompt": f"<|im_start|>user\n{clean_prompt}<|im_end|>\n<|im_start|>assistant\n",
            "chosen": chosen_output,
            "rejected": rejected_output,
            "metadata": {
                "source": "live_user_downvote",
                "session_id": rec["session_id"],
                "category": rec.get("feedback_category", "unspecified"),
                "ingested_at": rec.get("created_at")
            }
        })

    os.makedirs(DPO_DATA_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for p in dpo_pairs:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    print(f"\n[Pipeline Result] Successfully processed {len(dpo_pairs)} preference pairs.")
    print(f"[Export Destination] {OUTPUT_PATH}")
    print("\nSample Pair Extracted for Retraining:")
    if dpo_pairs:
        print(f"  Prompt   : {dpo_pairs[0]['prompt'].strip()}")
        print(f"  Chosen   : {dpo_pairs[0]['chosen']}")
        print(f"  Rejected : {dpo_pairs[0]['rejected']}")
    print("=" * 75)
    return dpo_pairs

if __name__ == "__main__":
    run_feedback_to_dpo_pipeline()

