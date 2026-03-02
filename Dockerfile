FROM python:3.12-slim-trixie as builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


WORKDIR /app

COPY ./src ./
COPY pyproject.toml uv.lock ./

RUN uv sync --locked


CMD ["uv", "run", "main.py"]
