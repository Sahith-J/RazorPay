from fastapi import APIRouter

from app.tools.orders import list_orders, get_order
from app.tools.products import list_products, get_product
from app.tools.inventory import get_inventory

router = APIRouter()


@router.get("/orders")
async def orders():
    return await list_orders()


@router.get("/orders/{order_id}")
async def order(order_id: int):
    return await get_order(order_id)


@router.get("/products")
async def products():
    return await list_products()


@router.get("/products/{product_id}")
async def product(product_id: int):
    return await get_product(product_id)


@router.get("/products/{product_id}/inventory")
async def inventory(product_id: int):
    return await get_inventory(product_id)