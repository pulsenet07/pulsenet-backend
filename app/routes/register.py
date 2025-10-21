import uuid
from fastapi import APIRouter
from app.db import conn, cursor
from datetime import datetime
from app.utils.auth import generate_api_key

router = APIRouter()

@router.post("/api/register")
async def register_agent(payload: dict):
    agent_id = payload.get("agent_id") or f"agent-{uuid.uuid4().hex[:8]}"
    fingerprint = payload.get("fingerprint")

    # create API key
    api_key = generate_api_key(agent_id)

    # store in DB (optional)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id SERIAL PRIMARY KEY,
            agent_id VARCHAR(100),
            api_key TEXT,
            fingerprint TEXT,
            registered_at TIMESTAMP
        )
    """)
    conn.commit()

    cursor.execute("""
        INSERT INTO agents (agent_id, api_key, fingerprint, registered_at)
        VALUES (%s, %s, %s, %s)
    """, (agent_id, api_key, fingerprint, datetime.utcnow()))
    conn.commit()

    print(f"[REGISTERED] New agent {agent_id}")
    return {"agent_id": agent_id, "api_key": api_key}
