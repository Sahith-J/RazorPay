from app.tools.orders import get_order
from app.tools.inventory import get_inventory


async def check_order_inventory(order_id: int) -> dict:
    order = await get_order(order_id)

    products = []

    for item in order.get("items", []):
        inventory = await get_inventory(item["product_id"])

        products.append(
            {
                "product_id": item["product_id"],
                "name": item["name"],
                "sku": item.get("sku"),
                "ordered_quantity": item["quantity"],
                "stock_status": inventory.get("stock_status"),
                "stock_quantity": inventory.get("stock_quantity"),
                "enough_stock": (
                    inventory.get("stock_quantity") is not None
                    and inventory.get("stock_quantity") >= item["quantity"]
                ),
            }
        )

    all_available = all(
        product["enough_stock"]
        for product in products
    )

    return {
        "order_id": order["id"],
        "order_number": order["number"],
        "order_status": order["status"],
        "all_items_available": all_available,
        "products": products,
    }