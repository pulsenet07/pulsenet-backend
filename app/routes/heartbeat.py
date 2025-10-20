from fastapi import APIRouter, Request, Header, HTTPException
from app.db import conn, cursor
from app.models import init_tables
from app.services.intelligence import calculate_health
from app.services.alerts import create_alert
from app.utils.auth import verify_api_key

router = APIRouter()

init_tables(cursor)
conn.commit()

@router.post("/api/heartbeat")
async def receive_heartbeat(req: Request, authorization: str = Header(None)):
    data = await req.json()

    if authorization:
        token = authorization.replace("Bearer ", "")
        agent_id = verify_api_key(token)
        if not agent_id:
            raise HTTPException(status_code=401, detail="Invalid or expired API key")
    else:
        agent_id = data["agent_id"]  # allow self-hosted mode
    
    metrics = data["metrics"]

    cpu = metrics["cpu"]
    memory = metrics["memory"]
    disk = metrics["disk"]

    health = calculate_health(cpu, memory, disk)

    # Save pulse
    cursor.execute("""
        INSERT INTO pulses (agent_id, timestamp, cpu, memory, disk, network_in, network_out, uptime, status, health_score)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        agent_id, data["timestamp"], cpu, memory, disk,
        metrics["network"]["in_kbps"], metrics["network"]["out_kbps"],
        metrics["uptime"], data["status"], health
    ))
    conn.commit()

    # === ALERT CONDITIONS ===
    if health < 40:
        create_alert(
            data["agent_id"],
            alert_type="low_health",
            description=f"Server health dropped critically low ({health}%)",
            severity="high" if health < 40 else "medium"
        )

    if cpu > 90:
        create_alert(data["agent_id"], "high_cpu", f"CPU usage at {cpu}%", "medium")

    if memory > 90:
        create_alert(data["agent_id"], "high_memory", f"Memory usage at {memory}%", "medium")

    if disk > 90:
        create_alert(data["agent_id"], "disk_full", f"Disk usage at {disk}%", "medium")

    return {"msg": "pulse received", "health": health}
