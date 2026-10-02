import json

from ollama import AsyncClient

from app.tools.order_inventory import check_order_inventory

from app.config import settings
from app.tools.orders import (
    list_orders,
    get_order,
    search_orders,
)
from app.tools.products import (
    list_products,
    get_product,
    search_products,
)
from app.tools.inventory import get_inventory


client = AsyncClient(
    host=settings.ollama_host,
)


SYSTEM_PROMPT = """
You are a read-only WooCommerce merchant support agent.

IMPORTANT RULES:

1. For any question about whether items in an order are in stock,
   ALWAYS use wc_check_order_inventory.

2. Never calculate or guess stock quantities yourself.

3. Never change product IDs, SKUs, quantities, prices, statuses,
   customer information, or tool results.

4. Every factual statement about WooCommerce must come from a tool result.

5. Do not say "I will check", "let's check", or "I'll proceed".
   Call the required tool first, then give the final answer.

6. This connector is read-only. Never claim that anything was modified.

7. If a tool reports outofstock, describe the product as out of stock.

8. When enough_stock is false, clearly say there is not enough current
   inventory to fulfil that line item.

9. Keep the final answer concise.
"""

async def wc_check_order_inventory(order_id: int):
    """
    Check whether all products in a WooCommerce order
    currently have enough stock.

    Args:
        order_id: Numeric WooCommerce order ID.
    """
    return await check_order_inventory(order_id)


async def wc_list_orders(
    page: int = 1,
    per_page: int = 10,
    status: str | None = None,
):
    """List WooCommerce orders."""
    return await list_orders(
        page=page,
        per_page=per_page,
        status=status,
    )


async def wc_get_order(order_id: int):
    """Get a WooCommerce order by ID."""
    return await get_order(order_id)


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


async def wc_list_products(
    page: int = 1,
    per_page: int = 10,
):
    """List WooCommerce products."""
    return await list_products(
        page=page,
        per_page=per_page,
    )


async def wc_get_product(product_id: int):
    """Get a WooCommerce product by ID."""
    return await get_product(product_id)


async def wc_search_products(
    search: str,
    page: int = 1,
    per_page: int = 10,
):
    """Search WooCommerce products."""
    return await search_products(
        search=search,
        page=page,
        per_page=per_page,
    )


async def wc_get_inventory(product_id: int):
    """Get stock information for a WooCommerce product."""
    return await get_inventory(product_id)


TOOLS = [
    wc_list_orders,
    wc_get_order,
    wc_search_orders,
    wc_list_products,
    wc_get_product,
    wc_search_products,
    wc_check_order_inventory,
    wc_get_inventory,
]


TOOL_MAP = {
    "wc_list_orders": wc_list_orders,
    "wc_get_order": wc_get_order,
    "wc_search_orders": wc_search_orders,
    "wc_list_products": wc_list_products,
    "wc_get_product": wc_get_product,
    "wc_search_products": wc_search_products,
    "wc_get_inventory": wc_get_inventory,
    "wc_check_order_inventory": wc_check_order_inventory,
}


async def run_agent(message: str):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": message,
        },
    ]

    activities = []

    for _ in range(8):
        response = await client.chat(
            model=settings.ollama_model,
            messages=messages,
            tools=TOOLS,
        )

        assistant_message = response.message
        tool_calls = assistant_message.tool_calls or []

        messages.append(
            {
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": tool_calls,
            }
        )

        if not tool_calls:
            return {
                "answer": assistant_message.content,
                "activities": activities,
            }

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments or {}

            activities.append(
                {
                    "tool": tool_name,
                    "arguments": arguments,
                }
            )

            tool_function = TOOL_MAP.get(tool_name)

            if tool_function is None:
                tool_result = {
                    "error": f"Unknown tool: {tool_name}"
                }
            else:
                try:
                    tool_result = await tool_function(**arguments)
                except Exception as exc:
                    tool_result = {
                        "error": str(exc)
                    }

            messages.append(
                {
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": json.dumps(tool_result),
                }
            )

    return {
        "answer": (
            "I reached the maximum number of tool calls "
            "before completing the request."
        ),
        "activities": activities,
    }