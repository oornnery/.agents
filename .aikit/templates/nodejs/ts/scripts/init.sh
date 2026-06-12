#!/usr/bin/env bash
set -euo pipefail

echo "Installing dependencies..."
npm install

echo "Running validation checks..."
npm run check

echo "Setup complete."
