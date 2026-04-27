# Security Audit Report

## Summary

`request changes`

review found one high-severity authorization gap and one medium-severity
logging issue.

## Findings

- Rule ID: SEC-001
  Severity: High
  Location: `src/myapp/api/payments.py:42`
  Evidence: payment detail endpoint loads by ID without checking tenant or owner
  Impact: cross-tenant data exposure
  Fix: enforce object-level authorization before returning record
- Rule ID: SEC-014
  Severity: Medium
  Location: `src/myapp/auth/session.py:18`
  Evidence: raw session token is logged on auth failure
  Impact: token leakage into logs
  Fix: log only token fingerprint or request metadata
