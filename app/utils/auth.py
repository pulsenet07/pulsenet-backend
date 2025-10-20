import jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"

def generate_api_key(agent_id: str):
    payload = {
        "agent_id": agent_id,
        "exp": datetime.utcnow() + timedelta(days=365),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_api_key(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("agent_id")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
