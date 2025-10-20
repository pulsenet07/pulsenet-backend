from app.db import conn, cursor
from datetime import datetime

def create_alert(agent_id, alert_type, description, severity="medium"):
    cursor.execute("""
        INSERT INTO alerts (agent_id, timestamp, alert_type, description, severity)
        VALUES (%s, %s, %s, %s, %s)
    """, (agent_id, datetime.utcnow(), alert_type, description, severity))
    conn.commit()
    print(f"[ALERT] [{severity.upper()}] {description} (agent: {agent_id})")
