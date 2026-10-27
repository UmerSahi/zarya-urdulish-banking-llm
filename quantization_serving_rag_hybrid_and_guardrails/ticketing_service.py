"""
Ticketing & Human Escalation Service (Day 4 Task 5)
Client: Zarya Digital Bank (Pakistan)
Features:
- Translates model structured JSON into official banking ticket
- Evaluates escalation criteria: Fraud, High Value (> PKR 50,000), Angry Sentiment, Urgent Card Theft
- Dispatches ticket to core database and returns SBP Turnaround Time (TAT)
"""

import os
import random
from typing import Dict, Any, Tuple
from database import insert_ticket, init_db

init_db()

def process_ticket_triage(
    structured_json: Dict[str, Any],
    customer_phone: str = "0300-1234567",
    raw_query: str = ""
) -> Tuple[Dict[str, Any], bool, str]:
    """
    Evaluates escalation conditions and persists ticket.
    Returns: (ticket_record, is_escalated, escalation_reason)
    """
    category = structured_json.get("category", "transfers_payments")
    sub_category = structured_json.get("sub_category", "general_dispute")
    urgency = structured_json.get("urgency", "medium")
    sentiment = structured_json.get("sentiment", "neutral")
    ticket_details = structured_json.get("ticket_details", {}) or {}

    ticket_id = ticket_details.get("ticket_id") or f"ZDB-{random.randint(10000000, 99999999)}"
    tat_hours = ticket_details.get("estimated_tat_hours", 24)
    priority = ticket_details.get("priority", "P3")
    summary = ticket_details.get("summary_english") or f"Dispute logged for {sub_category}"
    action_needed = ticket_details.get("action_needed") or "Verify 1Link switch transaction status"

    # -------------------------------------------------------------
    # ESCALATION ENGINE (State Bank & Bank Policy Rules)
    # -------------------------------------------------------------
    escalate_to_human = False
    escalation_reason = ""

    # Rule 1: Fraud / Unauthorized activity / Card theft
    if category == "fraud_security" or "unauthorized" in raw_query.lower() or "theft" in sub_category.lower():
        escalate_to_human = True
        priority = "P1"
        tat_hours = min(tat_hours, 4)
        escalation_reason = "CRITICAL: Security / Fraud / Unauthorized transaction detected"

    # Rule 2: Extreme anger / State Bank Mohtasib legal escalation threats
    elif sentiment in ["angry", "panicked"] or "state bank" in raw_query.lower() or "mohtasib" in raw_query.lower():
        escalate_to_human = True
        priority = "P1"
        tat_hours = min(tat_hours, 4)
        escalation_reason = "HIGH: Severe customer distress / SBP regulatory grievance threat"

    # Rule 3: High value transactions (> PKR 50,000)
    elif any(amt in raw_query for amt in ["50,000", "75,000", "100,000", "200,000", "lakh"]):
        escalate_to_human = True
        priority = "P2"
        escalation_reason = "HIGH VALUE: Dispute exceeds PKR 50,000 threshold"

    # Rule 4: Priority P1 tickets default to human desk
    elif priority == "P1":
        escalate_to_human = True
        escalation_reason = "Priority P1 automated desk escalation"

    status = "ESCALATED_HUMAN_AGENT" if escalate_to_human else "OPEN_IN_PROGRESS"

    ticket_record = {
        "ticket_id": ticket_id,
        "customer_phone": customer_phone,
        "category": category,
        "sub_category": sub_category,
        "priority": priority,
        "urgency": urgency,
        "tat_hours": tat_hours,
        "summary": summary,
        "action_needed": action_needed,
        "status": status,
        "escalated_to_human": escalate_to_human,
        "escalation_reason": escalation_reason,
        "customer_response": structured_json.get("customer_response_urdulish", "")
    }

    insert_ticket(ticket_record)
    return ticket_record, escalate_to_human, escalation_reason
