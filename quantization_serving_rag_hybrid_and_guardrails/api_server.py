"""
FastAPI Production Gateway: Connecting Guardrails -> RAG -> Model -> Ticketing Tools
Client: Zarya Digital Bank (Pakistan)
Task: Day 4 Task 5 — Production Serving API
"""

import os
import sys
import json
import time
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel, Field

from guardrails import BankingGuardrails
from rag_system import BankingRAGSystem
from ticketing_service import process_ticket_triage
from database import get_all_tickets

app = FastAPI(
    title="Zarya Digital Bank AI Support Gateway",
    description="Production API with input/output guardrails, RAG over live banking policies, and automated support ticketing.",
    version="1.0.0"
)

# Initialize engines
guardrails = BankingGuardrails()
rag_system = BankingRAGSystem()

# -----------------------------------------------------------------------------
# PYDANTIC SCHEMAS
# -----------------------------------------------------------------------------
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "zarya-qwen-2.5-3b-urdulish"
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.2
    max_tokens: Optional[int] = 256
    stream: Optional[bool] = False

class BankingQueryRequest(BaseModel):
    customer_phone: Optional[str] = "0300-1234567"
    message: str
    session_id: Optional[str] = "sess_default"

class BankingQueryResponse(BaseModel):
    response: str
    guardrail_status: str
    rag_sources: List[str]
    ticket_created: bool
    ticket_id: Optional[str] = None
    priority: Optional[str] = None
    estimated_tat_hours: Optional[int] = None
    escalated_to_human: bool = False
    escalation_reason: Optional[str] = None
    latency_ms: float

# -----------------------------------------------------------------------------
# ENDPOINTS
# -----------------------------------------------------------------------------
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Zarya AI Banking Gateway",
        "model": "Qwen 2.5 3B (DPO Aligned Q4_K_M)",
        "guardrails": "Active",
        "rag_kb_chunks": len(rag_system.chunks)
    }

@app.post("/api/chat", response_model=BankingQueryResponse)
def handle_customer_message(req: BankingQueryRequest):
    start_time = time.time()
    user_text = req.message

    # 1. INPUT GUARDRAILS
    input_audit = guardrails.process_input(user_text)
    if not input_audit["passed"]:
        elapsed = (time.time() - start_time) * 1000.0
        return BankingQueryResponse(
            response=input_audit["override_response"],
            guardrail_status=input_audit["action"],
            rag_sources=[],
            ticket_created=False,
            latency_ms=round(elapsed, 2)
        )

    clean_text = input_audit["sanitized_input"]

    # 2. RAG RETRIEVAL OVER BANKING POLICIES
    retrieved_chunks = rag_system.retrieve(clean_text, top_k=2)
    sources = [c["source"] for c in retrieved_chunks if c["score"] > 0.15]

    # 3. MODEL INFERENCE (Fine-Tuned + RAG Hybrid)
    raw_reply = rag_system.answer_with_hybrid_model(clean_text, model_mode="hybrid")

    # 4. OUTPUT GUARDRAILS (Scrub PII, mask 16-digit cards/CNICs)
    safe_reply = guardrails.process_output(raw_reply)

    # 5. AUTOMATED DISPUTE TICKETING & ESCALATION
    ticket_created = False
    ticket_id = None
    priority = None
    tat_hours = None
    escalated = False
    escalation_reason = None

    # Triage: if the query reports a dispute, failed transfer, lost card, or ATM issue
    is_dispute = any(w in clean_text.lower() for w in ["fail", "kat gaye", "block", "gum", "atm", "nahi niklay", "chori", "unpaid"])
    if is_dispute:
        ticket_created = True
        structured_triage = {
            "category": "cards_atm" if ("card" in clean_text.lower() or "atm" in clean_text.lower()) else "transfers_payments",
            "sub_category": "failed_transaction_or_card_issue",
            "urgency": "critical" if ("block" in clean_text.lower() or "chori" in clean_text.lower()) else "high",
            "sentiment": "panicked" if ("foran" in clean_text.lower() or "jaldi" in clean_text.lower()) else "anxious",
            "ticket_details": {
                "estimated_tat_hours": 24 if "raast" in clean_text.lower() else (72 if "card" in clean_text.lower() else 48),
                "priority": "P1" if "block" in clean_text.lower() else "P2",
                "summary_english": f"Customer reported: {clean_text[:60]}...",
                "action_needed": "Verify transaction settlement on 1Link switch"
            },
            "customer_response_urdulish": safe_reply
        }
        ticket_rec, escalated, escalation_reason = process_ticket_triage(
            structured_triage,
            customer_phone=req.customer_phone,
            raw_query=clean_text
        )
        ticket_id = ticket_rec["ticket_id"]
        priority = ticket_rec["priority"]
        tat_hours = ticket_rec["tat_hours"]

    elapsed = (time.time() - start_time) * 1000.0
    return BankingQueryResponse(
        response=safe_reply,
        guardrail_status=input_audit.get("flag", "PASSED"),
        rag_sources=sources,
        ticket_created=ticket_created,
        ticket_id=ticket_id,
        priority=priority,
        estimated_tat_hours=tat_hours,
        escalated_to_human=escalated,
        escalation_reason=escalation_reason,
        latency_ms=round(elapsed, 2)
    )

@app.post("/v1/chat/completions")
def openai_chat_completions(req: ChatCompletionRequest):
    """
    OpenAI-compatible chat completion endpoint for standard integrations.
    """
    last_user_msg = next((m.content for m in reversed(req.messages) if m.role == "user"), "")
    banking_resp = handle_customer_message(BankingQueryRequest(message=last_user_msg))
    
    return {
        "id": f"chatcmpl-zdb-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": banking_resp.response
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": len(last_user_msg.split()) * 2,
            "completion_tokens": len(banking_resp.response.split()) * 2,
            "total_tokens": (len(last_user_msg.split()) + len(banking_resp.response.split())) * 2
        }
    }

@app.get("/api/tickets")
def list_support_tickets(limit: int = 50):
    """
    Support agent dashboard endpoint to monitor incoming dispute tickets and escalations.
    """
    return {
        "total_tickets": len(get_all_tickets(limit)),
        "tickets": get_all_tickets(limit)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
