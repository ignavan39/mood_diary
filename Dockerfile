FROM python:3.12-slim AS builder
RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --locked

FROM python:3.12-slim AS runtime

WORKDIR /app

COPY . .

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

CMD ["python", "./src/main.py"]