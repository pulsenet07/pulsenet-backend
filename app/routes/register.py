from fastapi import APIRouter
from app.db import conn, cursor
from datetime import datetime
from app.utils.auth import generate_api_key

router = APIRouter()

@router.post("/api/register")
async def register_agent(payload: dict):
    agent_id = payload.get("agent_id")

    # create API key
    api_key = generate_api_key(agent_id)

    # store in DB (optional)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id SERIAL PRIMARY KEY,
            agent_id VARCHAR(100),
            api_key TEXT,
            registered_at TIMESTAMP
        )
    """)
    conn.commit()

    cursor.execute("""
        INSERT INTO agents (agent_id, api_key, registered_at)
        VALUES (%s, %s, %s)
    """, (agent_id, api_key, datetime.utcnow()))
    conn.commit()

    print(f"[REGISTERED] New agent {agent_id}")
    return {"agent_id": agent_id, "api_key": api_key}
