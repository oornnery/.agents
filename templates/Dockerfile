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

CMD ["uv", "run", "fastapi", "run", "--host", "0.0.0.0"]
