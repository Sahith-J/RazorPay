def serialize_order(order: dict) -> dict:
    billing = order.get("billing", {})

    customer_name = " ".join(
        part for part in [
            billing.get("first_name"),
            billing.get("last_name"),
        ]
        if part
    )

    return {
        "id": order.get("id"),
        "number": order.get("number"),
        "status": order.get("status"),
        "currency": order.get("currency"),
        "total": order.get("total"),
        "date_created": order.get("date_created"),
        "customer": {
            "name": customer_name,
            "email": billing.get("email"),
        },
        "items": [
            {
                "product_id": item.get("product_id"),
                "name": item.get("name"),
                "sku": item.get("sku"),
                "quantity": item.get("quantity"),
                "price": item.get("price"),
            }
            for item in order.get("line_items", [])
        ],
    }


def serialize_product(product: dict) -> dict:
    return {
        "id": product.get("id"),
        "name": product.get("name"),
        "sku": product.get("sku"),
        "price": product.get("price"),
        "regular_price": product.get("regular_price"),
        "stock_status": product.get("stock_status"),
        "stock_quantity": product.get("stock_quantity"),
        "manage_stock": product.get("manage_stock"),
    }