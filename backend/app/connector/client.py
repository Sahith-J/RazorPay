import asyncio
from typing import Any

import httpx

from app.config import settings
from app.connector.exceptions import (
    WooCommerceAPIError,
    WooCommerceAuthenticationError,
    WooCommerceNotFoundError,
    WooCommerceRateLimitError,
)


class WooCommerceClient:
    def __init__(self):
        self.base_url = (
            settings.woocommerce_url.rstrip("/")
            + "/wp-json/wc/v3"
        )

        self.auth = (
            settings.woocommerce_consumer_key,
            settings.woocommerce_consumer_secret,
        )

        self.timeout = settings.request_timeout
        self.max_retries = settings.max_retries

    async def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> Any:

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        async with httpx.AsyncClient(
        auth=self.auth,
        timeout=self.timeout,
        verify=settings.verify_ssl,
    ) as client:

            for attempt in range(self.max_retries + 1):

                response = await client.request(
                    method,
                    url,
                    params=params,
                )

                if response.status_code in (401, 403):
                    raise WooCommerceAuthenticationError(
                        "WooCommerce authentication failed."
                    )

                if response.status_code == 404:
                    raise WooCommerceNotFoundError(
                        f"Resource not found: {endpoint}"
                    )

                if response.status_code == 429:
                    if attempt >= self.max_retries:
                        raise WooCommerceRateLimitError(
                            "WooCommerce rate limit exceeded."
                        )

                    retry_after = response.headers.get("Retry-After")

                    delay = (
                        float(retry_after)
                        if retry_after
                        else 2 ** attempt
                    )

                    await asyncio.sleep(delay)
                    continue

                if 500 <= response.status_code < 600:
                    if attempt >= self.max_retries:
                        raise WooCommerceAPIError(
                            f"WooCommerce returned "
                            f"{response.status_code}"
                        )

                    await asyncio.sleep(2 ** attempt)
                    continue

                if response.is_error:
                    raise WooCommerceAPIError(
                        f"WooCommerce returned "
                        f"{response.status_code}: "
                        f"{response.text}"
                    )

                return response.json()

        raise WooCommerceAPIError(
            "WooCommerce request failed."
        )


woocommerce_client = WooCommerceClient()