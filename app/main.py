from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import heartbeat, register

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