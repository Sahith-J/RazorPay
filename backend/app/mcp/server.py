from fastmcp import FastMCP

from app.tools.orders import list_orders, get_order, search_orders
from app.tools.products import list_products, get_product, search_products
from app.tools.inventory import get_inventory
from app.tools.order_inventory import check_order_inventory

mcp = FastMCP("woocommerce-connector")


@mcp.tool
async def wc_list_orders(
    page: int = 1,
    per_page: int = 10,
    status: str | None = None,
):
    """List WooCommerce orders, optionally filtered by status."""
    return await list_orders(
        page=page,
        per_page=per_page,
        status=status,
    )

@mcp.tool
async def wc_check_order_inventory(order_id: int):
    """
    Check whether all items in an order currently
    have sufficient inventory.
    """
    return await check_order_inventory(order_id)


@mcp.tool
async def wc_get_order(order_id: int):
    """Get a WooCommerce order by ID."""
    return await get_order(order_id)


@mcp.tool
async def wc_search_orders(
    search: str,
    page: int = 1,
    per_page: int = 10,
):
    """Search WooCommerce orders."""
    return await search_orders(
        search=search,
        page=page,
        per_page=per_page,
    )


@mcp.tool
async def wc_list_products(
    page: int = 1,
    per_page: int = 10,
):
    """List products from the WooCommerce catalog."""
    return await list_products(
        page=page,
        per_page=per_page,
    )


@mcp.tool
async def wc_get_product(product_id: int):
    """Get a WooCommerce product by ID."""
    return await get_product(product_id)


@mcp.tool
async def wc_search_products(
    search: str,
    page: int = 1,
    per_page: int = 10,
):
    """Search the WooCommerce product catalog."""
    return await search_products(
        search=search,
        page=page,
        per_page=per_page,
    )


@mcp.tool
async def wc_get_inventory(product_id: int):
    """Get current stock information for a product."""
    return await get_inventory(product_id)


if __name__ == "__main__":
    mcp.run()