# Architecture

## Overview

The project is split into four layers:

```text
Frontend
   |
   v
Application / Agent Layer
   |
   v
Connector / Tool Layer
   |
   v
WooCommerce REST API
```

## 1. WooCommerce Client

The WooCommerce client is responsible for:

- authentication
- HTTP requests
- retries
- rate-limit handling
- upstream error normalization

It communicates with the WooCommerce REST API under:

```text
/wp-json/wc/v3
```

Authentication uses WooCommerce Consumer Key and Consumer Secret credentials.

## 2. Connector Tools

The connector exposes structured read-only primitives.

### Orders

```text
list_orders
get_order
search_orders
```

### Products

```text
list_products
get_product
search_products
```

### Inventory

```text
get_inventory
check_order_inventory
```

The tools return normalized objects instead of raw WooCommerce payloads.

This reduces irrelevant data and makes the connector easier for agents to use.

## 3. Higher-Level Merchant Workflow Tool

`check_order_inventory` is intentionally higher-level.

Instead of requiring an agent to:

```text
get_order
get_inventory
get_inventory
...
```

the agent can call:

```text
check_order_inventory(order_id)
```

The tool internally:

1. loads the order
2. extracts product IDs
3. reads inventory
4. compares ordered quantity against stock
5. returns a deterministic result

This reduces multi-step reasoning burden and helps smaller models stay grounded.

## 4. MCP Server

FastMCP exposes the connector tools over MCP.

The MCP server is the main connector interface and runs over stdio.

It allows an MCP-compatible client or agent to discover and invoke the tools.

## 5. Demo Agent

The demo agent runs locally through Ollama.

The agent:

1. receives natural-language merchant requests
2. chooses connector tools
3. executes tools
4. reads structured results
5. returns a merchant-facing answer

The local model is not required by the connector itself.

It exists only to demonstrate how an agent can use the connector.

## 6. FastAPI Layer

FastAPI provides development and demo endpoints such as:

```text
GET /api/health
GET /api/orders
GET /api/orders/{id}
GET /api/products
GET /api/products/{id}
GET /api/products/{id}/inventory
POST /api/chat
```

These endpoints are primarily used for development, testing, and the demo UI.

## 7. React Frontend

The React frontend displays:

- chat interface
- WooCommerce connection state
- tool activity
- connector results

The activity panel makes tool use visible during the demo.

## Data Flow

Example:

```text
User
 |
 | "Check whether everything in order 20 is in stock"
 v
React
 |
 v
POST /api/chat
 |
 v
Ollama Agent
 |
 v
wc_check_order_inventory(20)
 |
 v
WooCommerce Connector
 |
 v
WooCommerce REST API
 |
 v
Structured inventory result
 |
 v
Agent response
 |
 v
React UI
```

## Reliability

The HTTP client handles:

- `401` / `403` authentication failures
- `404` missing resources
- `429` rate limiting
- transient `5xx` responses

Retries use bounded exponential backoff.

When `Retry-After` is provided, the connector respects it.

## Security Model

The connector is intentionally read-only.

WooCommerce credentials should be generated with:

```text
Read
```

permission only.

The connector does not expose:

- order updates
- inventory mutations
- refunds
- payment operations
- customer modifications
- product changes

This reduces the blast radius of agent actions.