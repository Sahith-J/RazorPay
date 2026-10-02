class WooCommerceError(Exception):
    """Base WooCommerce connector exception."""


class WooCommerceAuthenticationError(WooCommerceError):
    """Raised when WooCommerce authentication fails."""


class WooCommerceRateLimitError(WooCommerceError):
    """Raised when the WooCommerce API rate limit is exceeded."""


class WooCommerceNotFoundError(WooCommerceError):
    """Raised when a WooCommerce resource cannot be found."""


class WooCommerceAPIError(WooCommerceError):
    """Raised for general WooCommerce API failures."""