FROM python:3.12-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install dependencies first (layer caching)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy source
COPY src/ src/
RUN uv sync --frozen --no-dev

EXPOSE 8000

# Default FastAPI entrypoint. Update the module path for your app.
CMD ["uv", "run", "fastapi", "run", "src/myapp/main.py", "--host", "0.0.0.0", "--port", "8000"]
