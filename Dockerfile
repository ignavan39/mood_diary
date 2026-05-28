# Dockerfile
FROM python:3.14-slim-trixie AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN uv sync --frozen --no-dev --no-install-project --no-editable

COPY ./src ./src
COPY alembic.ini ./

RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.14-slim-trixie AS runtime

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src ./src
COPY --from=builder /app/alembic.ini ./

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health/live || exit 1

CMD ["python", "-m", "src.main"]