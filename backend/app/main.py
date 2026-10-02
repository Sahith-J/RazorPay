from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.commerce import router as commerce_router
from app.api.health import router as health_router
from app.config import settings
from app.api.chat import router as chat_router

app = FastAPI(
    title="WooCommerce Agent Connector",
    version="1.0.0",
    description=(
        "Read-only WooCommerce connector built for "
        "Razorpay Agent Studio."
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    chat_router,
    prefix="/api",
)

app.include_router(
    health_router,
    prefix="/api",
)

app.include_router(
    commerce_router,
    prefix="/api",
)


@app.get("/")
async def root():
    return {
        "name": "WooCommerce Agent Connector",
        "status": "running",
    }