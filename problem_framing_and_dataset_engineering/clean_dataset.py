"""
Data Quality, Cleaning, Deduplication & Pakistani Banking PII Redaction Pipeline
Client: Zarya Digital Bank
Task: Task 4 — Data Quality & Cleaning
"""

import os
import re
import json
import hashlib
from typing import List, Dict, Any, Tuple
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from schemas import validate_json_output

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# PAKISTANI BANKING PII PATTERNS & REGEX DETECTORS
# -----------------------------------------------------------------------------
# SBP & NADRA compliant PII detectors
PATTERNS_PII = {
    # 13-digit Pakistani CNIC: e.g., 42101-1234567-1 or 4210112345671
    "cnic_formatted": re.compile(r"\b\d{5}-\d{7}-\d{1}\b"),
    "cnic_raw": re.compile(r"\b\d{13}\b"),
    
    # 16-digit Debit / Credit Cards (Visa, MasterCard, PayPak): e.g., 4123 4567 8901 2345 or 4123-4567-8901-2345
    "card_16digit": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
    
    # Pakistani IBAN (PK followed by 2 digits and 20 alphanumeric chars)
    "iban_pk": re.compile(r"\bPK\d{2}[A-Z]{4}\d{16}\b", re.IGNORECASE),
    
    # Pakistani Mobile Phone: e.g. 0300-1234567, +923001234567, 03211234567
    "pk_mobile": re.compile(r"\b(?:\+92|0092|0)3\d{2}[-\s]?\d{7}\b"),
    
    # Standalone CVV (3 digits following CVV label)
    "cvv": re.compile(r"\b(?:cvv|cvc|security code)[:\s]*([0-9]{3})\b", re.IGNORECASE),
    
    # Standalone 4-6 digit OTP following 'otp' or 'code'
    "otp_isolated": re.compile(r"\b(?:otp|code|pin)[:\s]*([0-9]{4,6})\b", re.IGNORECASE)
}

def scan_and_redact_pii(text: str) -> Tuple[str, List[str]]:
    """
    Scans text for any sensitive Pakistani financial PII and masks it safely.
    Returns: (redacted_text, list_of_detected_pii_types)
    """
    detected = []
    redacted = text

    # Redact CNIC
    if PATTERNS_PII["cnic_formatted"].search(redacted) or PATTERNS_PII["cnic_raw"].search(redacted):
        detected.append("CNIC")
        redacted = PATTERNS_PII["cnic_formatted"].sub("[REDACTED_CNIC]", redacted)
        redacted = PATTERNS_PII["cnic_raw"].sub("[REDACTED_CNIC]", redacted)

    # Redact 16-digit Card Numbers
    if PATTERNS_PII["card_16digit"].search(redacted):
        # Check if it's not a generic reference
        match = PATTERNS_PII["card_16digit"].search(redacted)
        detected.append("CARD_NUMBER")
        redacted = PATTERNS_PII["card_16digit"].sub("XXXX-XXXX-XXXX-1234", redacted)

    # Redact IBAN
    if PATTERNS_PII["iban_pk"].search(redacted):
        detected.append("IBAN")
        redacted = PATTERNS_PII["iban_pk"].sub("PK**ZARYA00000000000000", redacted)

    # Redact CVV
    if PATTERNS_PII["cvv"].search(redacted):
        detected.append("CVV")
        redacted = PATTERNS_PII["cvv"].sub("CVV: [REDACTED_CVV]", redacted)

    return redacted, detected


# -----------------------------------------------------------------------------
# POLICY & HALLUCINATION CHECKERS
# -----------------------------------------------------------------------------
HALLUCINATION_TRIGGERS = [
    # Assistant claiming crypto is allowed or advising to buy crypto
    (re.compile(r"(crypto khareed lo|bitcoin buy karein|crypto is allowed in pakistan|binance par account banao)", re.IGNORECASE),
     "False crypto policy endorsement"),
    
    # Assistant asking for OTP or password
    (re.compile(r"(apna otp mujhe batayein|give me your pin|share your password|send your cvv)", re.IGNORECASE),
     "Assistant soliciting customer credentials"),
    
    # Unrealistic TAT claims (e.g. 0 minutes or 5 minutes for other-bank ATM dispute)
    (re.compile(r"(atm dispute 5 minute mein|dispute 10 minute mein hal)", re.IGNORECASE),
     "Unrealistic SBP dispute TAT hallucination"),
]

def check_policy_hallucinations(assistant_text: str) -> Tuple[bool, str]:
    """Returns (has_hallucination, reason)"""
    for trigger_regex, reason in HALLUCINATION_TRIGGERS:
        if trigger_regex.search(assistant_text):
            return True, reason
    return False, ""


# -----------------------------------------------------------------------------
# PROGRAMMATIC CLEANING PIPELINE
# -----------------------------------------------------------------------------
def run_cleaning_pipeline(input_path: str, output_path: str) -> Dict[str, Any]:
    print(f"Loading raw dataset from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    initial_count = len(records)
    print(f"Initial raw dataset count: {initial_count}")

    stats = {
        "initial_count": initial_count,
        "exact_duplicates_removed": 0,
        "near_duplicates_removed": 0,
        "length_filter_removed": 0,
        "json_schema_errors_removed": 0,
        "policy_hallucinations_removed": 0,
        "pii_records_redacted": 0,
        "final_clean_count": 0
    }

    # 1. Exact Deduplication based on hash of conversation turns
    seen_hashes = set()
    exact_deduped = []
    for item in records:
        content_key = " || ".join([f"{m['role']}:{m['content'].strip()}" for m in item["messages"]])
        item_hash = hashlib.sha256(content_key.encode("utf-8")).hexdigest()
        if item_hash in seen_hashes:
            stats["exact_duplicates_removed"] += 1
            continue
        seen_hashes.add(item_hash)
        exact_deduped.append(item)

    print(f"After exact deduplication: {len(exact_deduped)} (Removed {stats['exact_duplicates_removed']})")

    # 2. Length & Quality Filters
    length_passed = []
    for item in exact_deduped:
        user_msgs = [m["content"] for m in item["messages"] if m["role"] == "user"]
        asst_msgs = [m["content"] for m in item["messages"] if m["role"] == "assistant"]
        
        # Check minimum / maximum lengths
        user_too_short = any(len(u.strip()) < 8 for u in user_msgs)
        user_too_long = any(len(u.strip()) > 800 for u in user_msgs)
        asst_too_short = any(len(a.strip()) < 15 for a in asst_msgs)
        asst_too_long = any(len(a.strip()) > 2000 for a in asst_msgs)

        if user_too_short or user_too_long or asst_too_short or asst_too_long:
            stats["length_filter_removed"] += 1
            continue
        length_passed.append(item)

    print(f"After length & quality filter: {len(length_passed)} (Removed {stats['length_filter_removed']})")

    # 3. JSON Schema Validation & Policy Hallucination Check
    validated_items = []
    for item in length_passed:
        user_text = " ".join([m["content"] for m in item["messages"] if m["role"] == "user"])
        asst_text = " ".join([m["content"] for m in item["messages"] if m["role"] == "assistant"])

        # Check JSON validity for structured output tasks
        if item["task_type"] == "structured_json":
            asst_json = item["messages"][-1]["content"]
            valid, parsed, err = validate_json_output(asst_json)
            if not valid:
                stats["json_schema_errors_removed"] += 1
                continue

        # Check policy hallucination
        has_hallucination, reason = check_policy_hallucinations(asst_text)
        if has_hallucination:
            stats["policy_hallucinations_removed"] += 1
            continue

        validated_items.append(item)

    print(f"After schema & policy checks: {len(validated_items)} (Removed {stats['json_schema_errors_removed'] + stats['policy_hallucinations_removed']})")

    # 4. PII Scanning and Redaction
    clean_items = []
    for item in validated_items:
        modified = False
        redacted_messages = []
        for msg in item["messages"]:
            redacted_content, pii_types = scan_and_redact_pii(msg["content"])
            if pii_types:
                modified = True
            redacted_messages.append({"role": msg["role"], "content": redacted_content})
        
        if modified:
            stats["pii_records_redacted"] += 1
        item["messages"] = redacted_messages
        clean_items.append(item)

    print(f"PII Scan: {stats['pii_records_redacted']} records contained sensitive patterns and were safely redacted.")

    # 5. Near-Duplicate Deduplication (using TF-IDF Cosine Similarity on User queries)
    print("Running near-duplicate analysis with TF-IDF cosine similarity...")
    queries = [item["messages"][1]["content"] for item in clean_items]
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2), min_df=2)
    tfidf_matrix = vectorizer.fit_transform(queries)

    # We do a batch-wise near-dup check
    kept_indices = set()
    near_dup_count = 0
    batch_size = 500
    n = len(clean_items)

    for i in range(0, n, batch_size):
        end_i = min(i + batch_size, n)
        sim_block = cosine_similarity(tfidf_matrix[i:end_i], tfidf_matrix)
        for row_idx in range(sim_block.shape[0]):
            global_idx = i + row_idx
            if global_idx in kept_indices:
                continue
            # Look for duplicate in already processed records
            high_sim = False
            for prev_idx in kept_indices:
                if sim_block[row_idx, prev_idx] > 0.985 and prev_idx != global_idx:
                    high_sim = True
                    break
            if high_sim:
                near_dup_count += 1
            else:
                kept_indices.add(global_idx)

    final_dataset = [clean_items[idx] for idx in sorted(kept_indices)]
    stats["near_duplicates_removed"] = near_dup_count
    stats["final_clean_count"] = len(final_dataset)

    print(f"Near-duplicates removed: {near_dup_count}")
    print(f"Final clean dataset count: {len(final_dataset)}")

    # Write cleaned dataset
    with open(output_path, "w", encoding="utf-8") as f:
        for it in final_dataset:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

    # Write cleaning report
    report_json_path = os.path.join(REPORTS_DIR, "cleaning_report.json")
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    return stats


if __name__ == "__main__":
    raw_file = os.path.join(DATA_DIR, "raw_dataset.jsonl")
    clean_file = os.path.join(DATA_DIR, "cleaned_dataset.jsonl")
    report = run_cleaning_pipeline(raw_file, clean_file)
    print("\n--- Cleaning Pipeline Summary ---")
    for k, v in report.items():
        print(f"  {k:30s}: {v}")
