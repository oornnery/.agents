# Python Observability

Logging, metrics, tracing, correlation, and production diagnostics.

## Use When

- adding structured logs
- adding metrics/traces
- debugging production behavior
- propagating correlation/request IDs
- instrumenting web, HTTP, DB, AI, workers
- reducing noisy/unsafe logs

## Principles

- one primary observability path
- structured logs over string blobs
- correlation IDs across boundaries
- low-cardinality metrics
- no secrets or raw attacker payloads in logs
- instrumentation at boundaries and key business events
- measure four golden signals: latency, traffic, errors, saturation

## Structured Logging

Required fields where applicable:

- timestamp
- level
- service/component
- event name
- request/correlation ID
- user/tenant class when safe
- operation/result
- duration
- error type

Log levels:

| Level     | Use                                                |
| --------- | -------------------------------------------------- |
| `DEBUG`   | local/internal detail; off by default in prod      |
| `INFO`    | normal lifecycle/business events                   |
| `WARNING` | abnormal but handled condition                     |
| `ERROR`   | failed operation needing investigation             |

## Correlation

- create/request correlation ID at ingress
- propagate through HTTP headers, task payloads, and logs
- store in context-local state for request/task duration
- include in errors and external calls

## Metrics

Use metrics for aggregate behavior, not per-user forensic detail.

Good labels:

- route/template
- method
- status class
- dependency name
- bounded outcome
- queue name

Bad labels:

- user ID
- email
- full URL with IDs
- exception message
- unbounded object IDs

## Tracing

Trace cross-service or multi-step flows:

- web request
- outbound HTTP call
- DB operation
- queue enqueue/process
- LLM/tool call
- expensive business operation

Keep span names stable and low-cardinality.

## Logfire

Use when project asks for Logfire or already depends on it:

- configure once at app startup
- instrument stdlib logging if needed
- use spans around key operations
- add custom metrics sparingly
- suppress noisy libraries
- test with `capfire` where available

## Integration Map

| Surface       | Instrument                                  |
| ------------- | ------------------------------------------- |
| FastAPI/web   | request middleware, route spans, exceptions |
| HTTP clients  | outbound request spans + status/duration    |
| DB            | query spans, slow query logs, pool metrics  |
| workers       | job lifecycle, retries, queue lag           |
| AI/LLM        | model, latency, tool calls, errors, tokens  |
| Gunicorn/proc | worker lifecycle, errors                    |

## Security

Never log:

- secrets/tokens/passwords
- session material
- raw PII unless approved
- full auth headers
- raw attacker-controlled blobs unless needed and bounded

Prefer IDs/classes/buckets over raw values.

## Testing

- assert key log events with structured fields
- test correlation propagation
- verify secrets are redacted
- check metrics labels are bounded
- use fake exporters/capture fixtures

## Review Checklist

- [ ] clear event names
- [ ] stable field names
- [ ] correlation ID present
- [ ] no secrets/PII leakage
- [ ] metrics labels bounded
- [ ] traces around external/slow ops
- [ ] noisy libraries suppressed
- [ ] failures observable without log spam
