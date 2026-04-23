# BFF

Use when frontend needs API shape that shouldn't leak raw backend structure.

## When to Use

- web/mobile need meaningfully different payloads
- one screen depends on several backend services
- frontend would orchestrate too much itself
- UI needs aggregation, reshaping, or view-specific contracts

## When Not to Use

- only one client exists and base API already fits
- BFF would only proxy requests unchanged
- layer adds latency/maintenance without simplifying clients

## Core Role

BFF is consumer-facing orchestration layer.

- backend services own core business capabilities
- BFF owns view-oriented aggregation and shaping
- clients stay simpler because contract matches the screen/flow
- domain rules stay in the right service; BFF should not become the real application core

## Design Workflow

1. identify which frontend/flow the BFF serves
2. list exact data the screen needs
3. map which services provide each part
4. define BFF contract around client need, not upstream payloads
5. keep orchestration explicit: fetch, combine, normalize, return
6. add caching/precomputation only where read pattern justifies it

## Contract Rules

- keep BFF consumer-focused
- aggregate only what UI actually needs
- avoid leaking raw internal service contracts straight through
- prefer stable response shapes over mirroring every upstream change
- normalize naming, nullability, and status semantics at boundary
- expose one clear contract per screen, workflow, or client capability

## Good Boundaries

- **Good**: product details page needs product, pricing, stock, recommendations in one payload
- **Good**: mobile needs compact summary while web needs richer detail
- **Bad**: BFF re-exports `/users` unchanged from user service
- **Bad**: pricing rules, inventory rules, order rules reimplemented in BFF

## Route Shape

Prefer routes describing client-facing resource/flow, not upstream service topology.

Examples:

- `GET /bff/dashboard`
- `GET /bff/products/{id}/detail`
- `POST /bff/checkout/preview`

Avoid routes leaking service structure:

- `GET /bff/catalog-service-product-and-pricing`

## Orchestration Patterns

Choose lightest composition shape that solves the need:

- simple fan-out: fetch from several services, combine results
- enrichment: fetch primary data, attach secondary context
- normalization: convert several upstream shapes into one stable client contract
- workflow projection: shape data around screen/task such as checkout or onboarding

Keep orchestration explicit and easy to trace. Hidden magic makes BFF failures harder to debug.

## Auth and Trust Boundaries

- BFF must preserve auth and authorization guarantees
- never widen access just because BFF can see multiple services
- forward only identity, claims, and headers actually needed
- keep service-to-service trust explicit
- redact or drop fields client should not see, even if upstream returns them

## Error Handling

- translate noisy upstream failures into client-appropriate error contract
- preserve enough detail for debugging without leaking internals
- define partial-failure behavior explicitly
- when one section can degrade gracefully, return that state intentionally instead of failing whole screen by accident
- timeouts/retries should reflect user-facing latency budgets, not backend optimism

## Performance and Caching

- measure fan-out cost before adding more calls
- cache only where read pattern is actually repeated
- prefer batching or backend aggregation over many serial calls
- keep timeout budgets explicit per upstream dependency
- avoid turning BFF into N+1 factory for client convenience

## Testing

Test BFF as contract and orchestration layer.

- contract tests for response shape and status codes
- integration tests with realistic upstream responses
- partial-failure tests when one dependency degrades
- auth tests for field visibility and access boundaries
- latency/timeout tests for critical fan-out flows

## Anti-Patterns

- pass-through endpoints pretending to be architecture
- business logic migrating from services into BFF over time
- one giant BFF serving every client/screen with no clear ownership
- exposing upstream field names and enums directly to clients
- adding BFF before actual frontend need is understood