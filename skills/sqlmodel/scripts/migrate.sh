#!/usr/bin/env bash
set -euo pipefail

run_alembic() {
  if command -v uv >/dev/null 2>&1; then
    uv run alembic "$@"
  else
    alembic "$@"
  fi
}

show_help() {
  cat <<'EOF'
Database Migration Helper

Usage: ./migrate.sh [command] [options]

Commands:
  init                  Initialize Alembic
  create <message>      Create a new migration
  upgrade               Upgrade to latest migration
  downgrade             Downgrade one migration
  current               Show current migration
  history               Show migration history
  test                  Test upgrade and downgrade
EOF
}

init_alembic() {
  echo "Initializing Alembic..."
  run_alembic init alembic
  echo "Alembic initialized."
  echo "Update alembic.ini and alembic/env.py before generating migrations."
}

create_migration() {
  if [ -z "${1:-}" ]; then
    echo "Migration message is required." >&2
    exit 1
  fi

  echo "Creating migration: $1"
  run_alembic revision --autogenerate -m "$1"
  echo "Migration created. Review it before applying."
}

upgrade_db() {
  echo "Upgrading database..."
  run_alembic upgrade head
}

downgrade_db() {
  echo "Downgrading database..."
  run_alembic downgrade -1
}

show_current() {
  run_alembic current
}

show_history() {
  run_alembic history --verbose
}

test_migration() {
  echo "Testing migration..."
  run_alembic upgrade head
  run_alembic downgrade -1
  run_alembic upgrade head
  echo "Migration test completed successfully."
}

case "${1:-}" in
  init)
    init_alembic
    ;;
  create)
    create_migration "${2:-}"
    ;;
  upgrade)
    upgrade_db
    ;;
  downgrade)
    downgrade_db
    ;;
  current)
    show_current
    ;;
  history)
    show_history
    ;;
  test)
    test_migration
    ;;
  help|--help|-h)
    show_help
    ;;
  *)
    echo "Unknown command: ${1:-}" >&2
    show_help
    exit 1
    ;;
esac
