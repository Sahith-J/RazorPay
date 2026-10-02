import pytest

import app.tools.order_inventory as module


@pytest.mark.asyncio
async def test_check_order_inventory(monkeypatch):
    async def fake_get_order(order_id):
        return {
            "id": 20,
            "number": "20",
            "status": "processing",
            "items": [
                {
                    "product_id": 13,
                    "name": "Wireless Keyboard",
                    "sku": "KB-001",
                    "quantity": 1,
                },
                {
                    "product_id": 15,
                    "name": "USB-C Hub",
                    "sku": "KB-002",
                    "quantity": 1,
                },
            ],
        }

    async def fake_get_inventory(product_id):
        if product_id == 13:
            return {
                "product_id": 13,
                "name": "Wireless Keyboard",
                "sku": "KB-001",
                "stock_status": "instock",
                "stock_quantity": 10,
                "manage_stock": True,
            }

        return {
            "product_id": 15,
            "name": "USB-C Hub",
            "sku": "KB-002",
            "stock_status": "outofstock",
            "stock_quantity": 0,
            "manage_stock": True,
        }

    monkeypatch.setattr(
        module,
        "get_order",
        fake_get_order,
    )

    monkeypatch.setattr(
        module,
        "get_inventory",
        fake_get_inventory,
    )

    result = await module.check_order_inventory(20)

    assert result["order_id"] == 20
    assert result["all_items_available"] is False
    assert result["products"][0]["enough_stock"] is True
    assert result["products"][1]["enough_stock"] is False