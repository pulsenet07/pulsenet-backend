from pydantic import BaseModel
from typing import Dict

class HeartbeatPayload(BaseModel):
    agent_id: str
    timestamp: str
    metrics: Dict
    status: str
