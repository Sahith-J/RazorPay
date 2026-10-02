import pytest

from app.tools.serializers import serialize_order


def test_serialize_order():
    raw_order = {
        "id": 20,
        "number": "20",
        "status": "processing",
        "currency": "INR",
        "total": "4298.00",
        "date_created": "2026-10-02T15:24:48",
        "billing": {
            "first_name": "Jeevan",
            "last_name": "Kumar",
            "email": "jeevan@test.local",
        },
        "line_items": [
            {
                "product_id": 13,
                "name": "Wireless Keyboard",
                "sku": "KB-001",
                "quantity": 1,
                "price": 2499,
            }
        ],
    }

    result = serialize_order(raw_order)

    assert result["id"] == 20
    assert result["customer"]["name"] == "Jeevan Kumar"
    assert result["items"][0]["product_id"] == 13
    assert result["items"][0]["name"] == "Wireless Keyboard"