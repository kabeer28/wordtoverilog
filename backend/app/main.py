from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.generate import router as generate_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(generate_router, prefix="/api/v1")


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/capabilities")
def capabilities() -> dict[str, list[str] | bool]:
    return {
        "verifiers": settings.enabled_verifiers,
        "iverilog_enabled": settings.enable_iverilog,
    }
