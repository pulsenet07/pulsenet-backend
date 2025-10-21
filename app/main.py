from fastapi import FastAPI
from app.db_check import ensure_database_integrity
from fastapi.middleware.cors import CORSMiddleware
from app.routes import heartbeat, register

ensure_database_integrity()

app = FastAPI(title="PulseNet Backend")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(heartbeat.router)
app.include_router(register.router)