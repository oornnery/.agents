# Threat Model

## Scope

- Web app with authenticated users
- Background worker for asynchronous jobs
- Third-party payment provider

## Assets

- user accounts
- payment records
- session tokens
- internal admin actions

## Entry Points

- login endpoint
- payment webhook
- admin dashboard
- file upload flow

## Trust Boundaries

- browser -> app
- app -> database
- app -> third-party payment API
- tenant -> tenant

## Threats

- broken object authorization on payment records
- forged webhooks without signature valid
- stored XSS in rich text notes
- file upload abuse and path traversal

## Controls

- signed webhook verification
- per-object authorization checks
- server-side valid and escaping
- upload size and type restrictions

## Residual Risk

- rate-limit coverage for login remains incomplete

## Mitigations

- add login throttling
- add explicit audit log entries for admin payment actions
