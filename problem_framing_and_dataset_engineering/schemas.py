"""
Banking Support Ticket & Dialogue Pydantic Schemas
Client: Zarya Digital Bank (Fictional Pakistani Digital Retail Bank)
Standard: State Bank of Pakistan (SBP) Consumer Protection & Dispute Guidelines
"""

import json
from enum import Enum
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator


class TicketCategory(str, Enum):
    TRANSFERS_PAYMENTS = "transfers_payments"
    CARDS_ATM = "cards_atm"
    ACCOUNT_BALANCE = "account_balance"
    LOANS_PRODUCTS = "loans_products"
    COMPLAINTS_DISPUTES = "complaints_disputes"
    FRAUD_SECURITY = "fraud_security"
    OUT_OF_SCOPE = "out_of_scope"


class TicketUrgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CustomerSentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    ANXIOUS = "anxious"
    WORRIED = "worried"
    FRUSTRATED = "frustrated"
    ANGRY = "angry"
    PANICKED = "panicked"


class TicketPriority(str, Enum):
    P1 = "P1"  # Emergency / Fraud / Unauthorized transaction / Lost Card (TAT < 2 hours)
    P2 = "P2"  # Raast / ATM failed cash retraction (TAT 24 - 48 hours)
    P3 = "P3"  # Account statement / Limit inquiry / Product query (TAT 48 - 72 hours)
    P4 = "P4"  # General feedback / Low priority request (TAT 3 - 5 days)


class TicketDetails(BaseModel):
    ticket_id: str = Field(
        ...,
        description="Format: ZDB-XXXXXXXX (e.g. ZDB-89234102)",
        pattern=r"^ZDB-[0-9]{8}$"
    )
    priority: TicketPriority = Field(..., description="Escalation priority P1, P2, P3, P4")
    estimated_tat_hours: int = Field(
        ...,
        ge=1,
        le=240,
        description="State Bank compliant estimated Turnaround Time in hours"
    )
    action_needed: str = Field(
        ...,
        description="Specific technical or operational action required by the banking back-office"
    )
    summary_english: str = Field(
        ...,
        description="Concise English summary of the issue for banking core ticketing logs"
    )


class BankingSupportTicket(BaseModel):
    """
    Standard output emitted by the fine-tuned model for structured intent classification
    and automated backend ticket creation in PostgreSQL.
    """
    intent: str = Field(..., description="Specific customer intent, e.g. report_failed_transfer, block_card")
    category: TicketCategory = Field(..., description="High-level category of the issue")
    sub_category: str = Field(..., description="Granular classification, e.g. raast_p2p_failure, card_theft")
    urgency: TicketUrgency = Field(..., description="Urgency level assessed from customer message")
    sentiment: CustomerSentiment = Field(..., description="Detected customer emotional state")
    requires_ticket: bool = Field(..., description="True if core banking ticket / human agent escalation is required")
    ticket_details: Optional[TicketDetails] = Field(
        None,
        description="Populated only if requires_ticket is True"
    )
    customer_response_urdulish: str = Field(
        ...,
        description="Direct empathetic, respectful response delivered to customer in UrduLish"
    )

    @field_validator("ticket_details")
    @classmethod
    def validate_ticket_requirement(cls, v, values):
        # In Pydantic v2, data is in info/values
        return v


class ConversationTurn(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class BankingDatasetItem(BaseModel):
    id: str = Field(..., description="Unique sample identifier (e.g. ZDB-TRN-0001)")
    task_type: Literal["faq", "complaint", "fraud_refusal", "multi_turn", "structured_json"]
    category: TicketCategory
    language: Literal["urdulish", "roman_urdu", "english", "mixed"]
    is_multi_turn: bool = False
    messages: List[ConversationTurn]
    metadata: dict = Field(default_factory=dict)


def validate_json_output(json_text: str) -> tuple[bool, Optional[BankingSupportTicket], str]:
    """
    Utility to validate raw LLM JSON strings against the BankingSupportTicket schema.
    Returns (is_valid, parsed_object, error_message).
    """
    # Clean possible markdown ticks
    cleaned = json_text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
        ticket = BankingSupportTicket(**data)
        return True, ticket, ""
    except Exception as e:
        return False, None, str(e)


if __name__ == "__main__":
    # Test valid sample
    sample_data = {
        "intent": "report_failed_raast_transfer",
        "category": "transfers_payments",
        "sub_category": "raast_p2p_failure",
        "urgency": "high",
        "sentiment": "anxious",
        "requires_ticket": True,
        "ticket_details": {
            "ticket_id": "ZDB-10492817",
            "priority": "P2",
            "estimated_tat_hours": 24,
            "action_needed": "Initiate Raast interbank settlement check with 1Link",
            "summary_english": "Customer Raast transfer of PKR 15,000 failed but account debited."
        },
        "customer_response_urdulish": "Ji pareshan na hon, aap ki raqam bilkul mehfooz hai. Ticket # ZDB-10492817 darj ho chuki hai. Raast dispute 24 ghante mein resolve ho jayega."
    }
    valid, res, err = validate_json_output(json.dumps(sample_data))
    print(f"Validation test: valid={valid}, err={err}")
