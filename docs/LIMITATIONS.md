# Limitations and Assumptions

## Read-Only Connector

The connector only reads WooCommerce data.

It cannot:

- modify orders
- change order status
- create refunds
- update inventory
- modify products
- modify customers
- process payments

This is intentional.

## WooCommerce Search Semantics

Search behavior depends on the capabilities of the WooCommerce REST API.

Natural-language customer lookup may not always map perfectly to WooCommerce search behavior.

For a production connector, more explicit customer and order lookup primitives may be useful.

## Pagination

List operations support pagination.

The current demo uses small page sizes and does not automatically exhaust every page.

A production connector could add helpers for page iteration where needed.

## Rate Limits

WooCommerce deployments may sit behind different hosting providers, proxies, or rate limits.

The connector handles HTTP `429` responses and respects `Retry-After` when available.

It also retries transient `5xx` failures.

The connector does not attempt to bypass rate limits.

## Local TLS

LocalWP commonly uses a self-signed TLS certificate.

For local development:

```env
VERIFY_SSL=false
```

This should not be used in production.

Production deployments should use valid TLS certificates and:

```env
VERIFY_SSL=true
```

## Local Agent Model

The demo uses:

```text
qwen2.5:1.5b
```

through Ollama.

Small local models may occasionally:

- choose an incorrect tool
- summarize a result poorly
- stop before completing a multi-step workflow
- hallucinate when given too many low-level operations

To reduce this risk, the connector includes higher-level deterministic tools such as:

```text
wc_check_order_inventory
```

The connector itself does not depend on Ollama.

A production Agent Studio environment could use the same MCP tools with a stronger model.

## Inventory Interpretation

`stock_quantity` may be unavailable when WooCommerce stock management is disabled for a product.

In that case, the connector can report stock status but may not know the exact available quantity.

## Product Variations

The current demo focuses mainly on simple WooCommerce products.

A production connector should explicitly handle:

- variable products
- variation-specific inventory
- bundled products
- composite products

## Authentication

The current implementation uses WooCommerce Consumer Key and Consumer Secret authentication.

Credentials are configured through environment variables.

A production multi-merchant deployment would need secure per-merchant credential storage, rotation, and revocation.

## Demo Data

All data used in the demo is fictional.

No real customer data is required or expected.