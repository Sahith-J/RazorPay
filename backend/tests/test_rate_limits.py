import httpx
import pytest
import respx

from app.connector.client import WooCommerceClient


@pytest.mark.asyncio
async def test_retries_after_rate_limit(monkeypatch):
    client = WooCommerceClient()
    client.max_retries = 2

    sleep_calls = []

    async def fake_sleep(seconds):
        sleep_calls.append(seconds)

    monkeypatch.setattr(
        "app.connector.client.asyncio.sleep",
        fake_sleep,
    )

    with respx.mock:
        route = respx.get(
            f"{client.base_url}/products"
        )

        route.side_effect = [
            httpx.Response(
                429,
                headers={
                    "Retry-After": "1"
                },
            ),
            httpx.Response(
                200,
                json=[
                    {
                        "id": 13,
                        "name": "Wireless Keyboard",
                    }
                ],
            ),
        ]

        result = await client.request(
            "GET",
            "/products",
        )

        assert result[0]["id"] == 13
        assert sleep_calls == [1.0]


@pytest.mark.asyncio
async def test_retries_after_server_error(monkeypatch):
    client = WooCommerceClient()
    client.max_retries = 2

    sleep_calls = []

    async def fake_sleep(seconds):
        sleep_calls.append(seconds)

    monkeypatch.setattr(
        "app.connector.client.asyncio.sleep",
        fake_sleep,
    )

    with respx.mock:
        route = respx.get(
            f"{client.base_url}/products"
        )

        route.side_effect = [
            httpx.Response(502),
            httpx.Response(
                200,
                json=[],
            ),
        ]

        result = await client.request(
            "GET",
            "/products",
        )

        assert result == []
        assert sleep_calls == [1]