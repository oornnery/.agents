# Findings

- Rule ID: SEC-021
  Severity: Critical
  Location: `src/myapp/admin/tasks.py:88`
  Evidence: shell command is built from user input and executed without safe
  argument separation
  Impact: command execution on the host
  Fix: replace shell composition with a fixed argv list and strict allowlist

- Rule ID: SEC-033
  Severity: Medium
  Location: `src/myapp/files/upload.py:27`
  Evidence: uploaded file type is trusted from extension only
  Impact: unsafe file content can reach downstream processors
  Fix: validate content type and storage path before processing
