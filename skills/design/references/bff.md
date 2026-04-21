# BFF

Use this reference when a frontend needs an API shape that should not leak the
raw structure of backend services.

## When to Use

- web and mobile need meaningfully different payloads
- one screen depends on several backend services
- the frontend would otherwise orchestrate too much itself
- the UI needs aggregation, reshaping, or view-specific data contracts

## When Not to Use

- only one client exists and the base API already fits
- the BFF would only proxy requests unchanged
- the layer adds latency and maintenance without simplifying clients

## Core Role

The BFF is a consumer-facing orchestration layer.

- backend services own core business capabilities
- the BFF owns view-oriented aggregation and shaping
- clients stay simpler because the contract matches the screen or flow
- domain rules stay in the right service; the BFF should not become the real application core

## Design Workflow

1. identify which frontend or flow the BFF serves
2. list the exact data the screen needs
3. map which services provide each part
4. define the BFF contract around the client need, not the upstream payloads
5. keep orchestration explicit: fetch, combine, normalize, return
6. add caching or precomputation only where the read pattern justifies it

## Contract Rules

- keep the BFF consumer-focused
- aggregate only what the UI actually needs
- avoid leaking raw internal service contracts straight through
- prefer stable response shapes over mirroring every upstream change
- normalize naming, nullability, and status semantics at the boundary
- expose one clear contract per screen, workflow, or client capability

## Good Boundaries

- **Good**: product details page needs product, pricing, stock, and recommendations in one payload
- **Good**: mobile app needs a compact summary while web needs richer detail
- **Bad**: BFF re-exports `/users` unchanged from the user service
- **Bad**: pricing rules, inventory rules, and order rules are reimplemented in the BFF

## Route Shape

Prefer routes that describe the client-facing resource or flow, not the upstream
service topology.

Examples:

- `GET /bff/dashboard`
- `GET /bff/products/{id}/detail`
- `POST /bff/checkout/preview`

Avoid routes that leak service structure:

- `GET /bff/catalog-service-product-and-pricing`

## Orchestration Patterns

Choose the lightest composition shape that solves the need:

- simple fan-out: fetch from several services and combine results
- enrichment: fetch primary data, then attach secondary context
- normalization: convert several upstream shapes into one stable client contract
- workflow projection: shape data around a screen or task such as checkout or onboarding

Keep orchestration explicit and easy to trace. Hidden magic makes BFF failures
harder to debug.

## Auth and Trust Boundaries

- the BFF must preserve auth and authorization guarantees
- never widen access just because the BFF can see multiple services
- forward only the identity, claims, and headers that are actually needed
- keep service-to-service trust explicit
- redact or drop fields the client should not see, even if upstream returns them

## Error Handling

- translate noisy upstream failures into a client-appropriate error contract
- preserve enough detail for debugging without leaking internals
- define partial-failure behavior explicitly
- when one section can degrade gracefully, return that state intentionally instead of failing the whole screen by accident
- timeouts and retries should reflect user-facing latency budgets, not backend optimism

## Performance and Caching

- measure the fan-out cost before adding more calls
- cache only where the read pattern is actually repeated
- prefer batching or backend aggregation over many serial calls
- keep timeout budgets explicit per upstream dependency
- avoid turning the BFF into an N+1 factory for client convenience

## Testing

Test the BFF as a contract and orchestration layer.

- contract tests for response shape and status codes
- integration tests with realistic upstream responses
- partial-failure tests when one dependency degrades
- auth tests for field visibility and access boundaries
- latency or timeout tests for critical fan-out flows

## Anti-Patterns

- pass-through endpoints pretending to be architecture
- business logic migrating from services into the BFF over time
- one giant BFF serving every client and screen with no clear ownership
- exposing upstream field names and enums directly to clients
- adding a BFF before the actual frontend need is understood
