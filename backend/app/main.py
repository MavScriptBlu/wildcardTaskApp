"""
This is the starting point for the API.
It wires everything together:
CORS (so the frontend is allowed to talk to us), the task routes, and a health check endpoint for the container to ping.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasks

app = FastAPI(title="Task App API")

# Lets the frontend (running in a different container/port) call this API.
# FYI "*" is fine for a demo, but in production you should be more specific
# about which origins are allowed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)


@app.get("/health")
def health_check():
    """Quick way to check the API is alive."""
    return {"status": "ok"}


@app.get("/")
def root():
    """Simple landing route so hitting the base URL doesn't 404."""
    return {"message": "Task App API is running"}