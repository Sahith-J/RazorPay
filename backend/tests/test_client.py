import httpx
import pytest
import respx

from app.connector.client import WooCommerceClient
from app.connector.exceptions import (
    WooCommerceAuthenticationError,
    WooCommerceNotFoundError,
)


@pytest.mark.asyncio
async def test_successful_request(monkeypatch):
    client = WooCommerceClient()

    with respx.mock:
        route = respx.get(
            f"{client.base_url}/products"
        ).mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "id": 13,
                        "name": "Wireless Keyboard",
                    }
                ],
            )
        )

        result = await client.request(
            "GET",
            "/products",
        )

        assert route.called
        assert result[0]["id"] == 13


@pytest.mark.asyncio
async def test_authentication_failure():
    client = WooCommerceClient()

    with respx.mock:
        respx.get(
            f"{client.base_url}/products"
        ).mock(
            return_value=httpx.Response(
                401,
                json={
                    "message": "Unauthorized"
                },
            )
        )

        with pytest.raises(
            WooCommerceAuthenticationError
        ):
            await client.request(
                "GET",
                "/products",
            )


@pytest.mark.asyncio
async def test_not_found():
    client = WooCommerceClient()

    with respx.mock:
        respx.get(
            f"{client.base_url}/orders/9999"
        ).mock(
            return_value=httpx.Response(
                404,
                json={
                    "message": "Order not found"
                },
            )
        )

        with pytest.raises(
            WooCommerceNotFoundError
        ):
            await client.request(
                "GET",
                "/orders/9999",
            )