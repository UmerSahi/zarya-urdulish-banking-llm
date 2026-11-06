"""
Production FastAPI Gateway: Zarya Digital Bank (Pakistan)
Week 10 Capstone — Day 5: Enterprise Deployment & Serving Gateway
Features:
- OpenAI-compatible chat completions (/v1/chat/completions) with streaming
- High-performance customer banking endpoint (/api/chat)
- Guardrails -> RAG -> ModelService -> Support Ticketing -> Database Telemetry
- Human-in-the-loop support agent ticket management (/api/tickets)
- User feedback ingestion for continuous DPO training (/api/feedback)
- Full health & telemetry monitoring (/health, /api/metrics)
"""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import time
import json
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from database import (
    init_db, insert_ticket, get_all_tickets, update_ticket_status,
    log_telemetry, record_feedback, get_dashboard_metrics, get_feedback_records
)
from model_service import get_model_service

app = FastAPI(
    title="Zarya Digital Bank AI Support Gateway",
    description="Enterprise LLM Gateway with SBP Guardrails, Hybrid Policy RAG, and Automated Dispute Ticketing",
    version="2.0.0"
)

# Enable CORS for Streamlit and web frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database & model service on startup
init_db()
model_service = get_model_service()

# -----------------------------------------------------------------------------
# PYDANTIC DATA MODELS
# -----------------------------------------------------------------------------
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "zarya-qwen-2.5-3b-urdulish-dpo"
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.2
    max_tokens: Optional[int] = 256
    stream: Optional[bool] = False

class BankingQueryRequest(BaseModel):
    customer_phone: Optional[str] = "0300-1234567"
    message: str
    session_id: Optional[str] = "sess_web_client"

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
    prompt_tokens: int
    completion_tokens: int

class FeedbackRequest(BaseModel):
    session_id: str
    user_query: str
    assistant_response: str
    rating: int = Field(..., description="+1 for positive, -1 for negative")
    feedback_category: Optional[str] = "general"
    comment: Optional[str] = None

class TicketStatusUpdate(BaseModel):
    status: str

# -----------------------------------------------------------------------------
# HEALTH & METRICS ENDPOINTS
# -----------------------------------------------------------------------------
@app.get("/health")
def health_check():
    """Enterprise health verification for Kubernetes / Docker healthchecks."""
    return {
        "status": "healthy",
        "service": "Zarya AI Banking Serving Gateway",
        "model_engine": "Qwen 2.5 3B (LoRA + DPO Aligned)",
        "quantization": model_service.quant_method,
        "guardrails": "Active (State Bank of Pakistan Compliant)",
        "rag_kb_status": "Loaded (4 core banking policy modules)",
        "uptime": "Operational"
    }

@app.get("/api/metrics")
def get_metrics():
    """Real-time production metrics for analytics and monitoring dashboards."""
    return get_dashboard_metrics()

# -----------------------------------------------------------------------------
# CORE BANKING CONVERSATION ENDPOINTS
# -----------------------------------------------------------------------------
@app.post("/api/chat", response_model=BankingQueryResponse)
def handle_customer_message(req: BankingQueryRequest, background_tasks: BackgroundTasks):
    """
    Main customer chat endpoint connecting Guardrails -> RAG -> Model -> Ticketing -> Telemetry.
    """
    user_text = req.message.strip()
    if not user_text:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # Generate response via ModelService
    result = model_service.generate_response(user_text)

    # If dispute ticket was created, insert into database
    ticket_id = None
    priority = None
    tat_hours = None
    escalated = False
    escalation_reason = None

    if result.get("ticket_created") and result.get("ticket_info"):
        t_info = result["ticket_info"]
        t_info["customer_phone"] = req.customer_phone
        insert_ticket(t_info)
        ticket_id = t_info["ticket_id"]
        priority = t_info["priority"]
        tat_hours = t_info["tat_hours"]
        escalated = t_info["escalated_to_human"]
        escalation_reason = t_info.get("escalation_reason")

    # Asynchronous Telemetry Logging (PII Safe)
    masked_phone = req.customer_phone[:4] + "-XXXXXXX" if req.customer_phone else "03XX-XXXXXXX"
    telemetry_data = {
        "session_id": req.session_id,
        "customer_phone": masked_phone,
        "user_message": user_text,
        "assistant_response": result["response"],
        "guardrail_status": result["guardrail_status"],
        "rag_sources": json.dumps(result["rag_sources"]),
        "latency_ms": result["latency_ms"],
        "prompt_tokens": result["prompt_tokens"],
        "completion_tokens": result["completion_tokens"]
    }
    background_tasks.add_task(log_telemetry, telemetry_data)

    return BankingQueryResponse(
        response=result["response"],
        guardrail_status=result["guardrail_status"],
        rag_sources=result["rag_sources"],
        ticket_created=result["ticket_created"],
        ticket_id=ticket_id,
        priority=priority,
        estimated_tat_hours=tat_hours,
        escalated_to_human=escalated,
        escalation_reason=escalation_reason,
        latency_ms=result["latency_ms"],
        prompt_tokens=result["prompt_tokens"],
        completion_tokens=result["completion_tokens"]
    )

@app.post("/v1/chat/completions")
def openai_chat_completions(req: ChatCompletionRequest):
    """
    OpenAI-compatible chat completion endpoint.
    Allows seamless integration with standard OpenAI SDK, LangChain, or Chat UI tools.
    """
    last_user_msg = next((m.content for m in reversed(req.messages) if m.role == "user"), "")
    if not last_user_msg:
        raise HTTPException(status_code=400, detail="No user message provided.")

    if req.stream:
        # Streaming response generator
        def event_stream():
            result = model_service.generate_response(last_user_msg, enable_network_jitter=False)
            reply = result["response"]
            words = reply.split(" ")
            for w in words:
                chunk = {
                    "id": f"chatcmpl-{int(time.time())}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": req.model,
                    "choices": [{
                        "index": 0,
                        "delta": {"content": w + " "},
                        "finish_reason": None
                    }]
                }
                yield f"data: {json.dumps(chunk)}\n\n"
                time.sleep(0.02)
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    # Non-streaming response
    res = model_service.generate_response(last_user_msg)
    return {
        "id": f"chatcmpl-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": res["response"]
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": res["prompt_tokens"],
            "completion_tokens": res["completion_tokens"],
            "total_tokens": res["prompt_tokens"] + res["completion_tokens"]
        }
    }

# -----------------------------------------------------------------------------
# SUPPORT AGENT CRM DASHBOARD & FEEDBACK ENDPOINTS
# -----------------------------------------------------------------------------
@app.get("/api/tickets")
def list_tickets(limit: int = 50):
    """Retrieves all active support tickets and human escalations for agents."""
    tickets = get_all_tickets(limit)
    return {
        "total": len(tickets),
        "tickets": tickets
    }

@app.put("/api/tickets/{ticket_id}/status")
def update_ticket(ticket_id: str, update: TicketStatusUpdate):
    """Allows human support agent to update ticket status (e.g. In Progress, Resolved)."""
    success = update_ticket_status(ticket_id, update.status)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return {"status": "success", "ticket_id": ticket_id, "new_status": update.status}

@app.post("/api/feedback")
def submit_feedback(fb: FeedbackRequest):
    """
    Collects user thumbs up / down feedback.
    Negative ratings are automatically flagged for the Day 5 Task 2 DPO retraining pipeline.
    """
    feedback_id = record_feedback(fb.dict())
    return {
        "status": "success",
        "feedback_id": feedback_id,
        "flagged_for_dpo": fb.rating < 0
    }

@app.get("/api/feedback/flagged")
def list_flagged_feedback(limit: int = 50):
    """Returns feedback flagged for continuous DPO alignment."""
    records = get_feedback_records(only_flagged=True, limit=limit)
    return {
        "total_flagged": len(records),
        "records": records
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

