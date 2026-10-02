from app.tools.serializers import serialize_product


def test_serialize_product():
    raw_product = {
        "id": 13,
        "name": "Wireless Keyboard",
        "sku": "KB-001",
        "price": "2499",
        "regular_price": "2499",
        "stock_status": "instock",
        "stock_quantity": 10,
        "manage_stock": True,
    }

    result = serialize_product(raw_product)

    assert result == {
        "id": 13,
        "name": "Wireless Keyboard",
        "sku": "KB-001",
        "price": "2499",
        "regular_price": "2499",
        "stock_status": "instock",
        "stock_quantity": 10,
        "manage_stock": True,
    }