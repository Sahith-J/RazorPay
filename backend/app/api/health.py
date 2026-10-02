from fastapi import APIRouter

from app.connector.client import woocommerce_client

router = APIRouter()


@router.get("/health")
async def health():

    try:
        await woocommerce_client.request(
            "GET",
            "/products",
            params={"per_page": 1},
        )

        return {
            "status": "ok",
            "woocommerce": "connected",
        }

    except Exception as exc:
        return {
            "status": "error",
            "woocommerce": "disconnected",
            "error": str(exc),
        }