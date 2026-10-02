from typing import Any

from app.tools.products import get_product


async def get_inventory(
    product_id: int,
) -> dict[str, Any]:

    product = await get_product(product_id)

    return {
        "product_id": product["id"],
        "name": product["name"],
        "sku": product.get("sku"),
        "stock_status": product.get("stock_status"),
        "stock_quantity": product.get("stock_quantity"),
        "manage_stock": product.get("manage_stock"),
    }