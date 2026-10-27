"""
Core Banking Ticket Database Layer (SQLite / PostgreSQL compatible)
Client: Zarya Digital Bank (Pakistan)
Task: Day 4 Task 5 — Ticketing & Tools
"""

import os
import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "zarya_support.db")

def init_db(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS support_tickets (
        ticket_id TEXT PRIMARY KEY,
        customer_phone TEXT,
        category TEXT NOT NULL,
        sub_category TEXT,
        priority TEXT NOT NULL,
        urgency TEXT NOT NULL,
        tat_hours INTEGER NOT NULL,
        summary TEXT NOT NULL,
        action_needed TEXT,
        status TEXT NOT NULL,
        escalated_to_human BOOLEAN NOT NULL DEFAULT 0,
        customer_response TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()
    print(f"[Database] Support ticketing schema initialized at {db_path}")

def insert_ticket(ticket_data: Dict[str, Any], db_path: str = DB_PATH) -> bool:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO support_tickets (
        ticket_id, customer_phone, category, sub_category, priority,
        urgency, tat_hours, summary, action_needed, status,
        escalated_to_human, customer_response, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket_data["ticket_id"],
        ticket_data.get("customer_phone", "03XX-XXXXXXX"),
        ticket_data["category"],
        ticket_data.get("sub_category", "general"),
        ticket_data["priority"],
        ticket_data["urgency"],
        ticket_data["tat_hours"],
        ticket_data["summary"],
        ticket_data.get("action_needed", "Review customer dispute"),
        ticket_data["status"],
        1 if ticket_data.get("escalated_to_human", False) else 0,
        ticket_data.get("customer_response", ""),
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()
    return True

def get_all_tickets(limit: int = 50, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM support_tickets ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
