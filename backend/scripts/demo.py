import asyncio
import json

from app.tools.orders import get_order
from app.tools.products import search_products
from app.tools.order_inventory import check_order_inventory


async def main():
    print("\nWooCommerce Connector Demo\n")

    print("1. Fetch order #20")
    order = await get_order(20)
    print(json.dumps(order, indent=2))

    print("\n2. Check inventory for order #20")
    inventory = await check_order_inventory(20)
    print(json.dumps(inventory, indent=2))

    print("\n3. Search for 'Wireless Keyboard'")
    products = await search_products("Wireless Keyboard")
    print(json.dumps(products, indent=2))


if __name__ == "__main__":
    asyncio.run(main())