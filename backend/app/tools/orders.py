from typing import Any

from app.connector.client import woocommerce_client
from app.tools.serializers import serialize_order


async def list_orders(
    page: int = 1,
    per_page: int = 10,
    status: str | None = None,
) -> list[dict[str, Any]]:

    params = {
        "page": page,
        "per_page": min(per_page, 100),
    }

    if status:
        params["status"] = status

    orders = await woocommerce_client.request(
        "GET",
        "/orders",
        params=params,
    )

    return [serialize_order(order) for order in orders]


async def get_order(order_id: int) -> dict[str, Any]:

    order = await woocommerce_client.request(
        "GET",
        f"/orders/{order_id}",
    )

    return serialize_order(order)


async def search_orders(
    search: str,
    page: int = 1,
    per_page: int = 10,
) -> list[dict[str, Any]]:

    orders = await woocommerce_client.request(
        "GET",
        "/orders",
        params={
            "search": search,
            "page": page,
            "per_page": min(per_page, 100),
        },
    )

    return [serialize_order(order) for order in orders]