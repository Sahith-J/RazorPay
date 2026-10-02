from typing import Any

from app.connector.client import woocommerce_client
from app.tools.serializers import serialize_product


async def list_products(
    page: int = 1,
    per_page: int = 10,
) -> list[dict[str, Any]]:

    products = await woocommerce_client.request(
        "GET",
        "/products",
        params={
            "page": page,
            "per_page": min(per_page, 100),
        },
    )

    return [serialize_product(product) for product in products]


async def get_product(
    product_id: int,
) -> dict[str, Any]:

    product = await woocommerce_client.request(
        "GET",
        f"/products/{product_id}",
    )

    return serialize_product(product)


async def search_products(
    search: str,
    page: int = 1,
    per_page: int = 10,
) -> list[dict[str, Any]]:

    products = await woocommerce_client.request(
        "GET",
        "/products",
        params={
            "search": search,
            "page": page,
            "per_page": min(per_page, 100),
        },
    )

    return [serialize_product(product) for product in products]