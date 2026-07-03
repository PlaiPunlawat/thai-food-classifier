FROM python:3.10-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY apps/api/pyproject.toml apps/api/uv.lock ./apps/api/

RUN --mount=type=cache,target=/root/.cache/uv \
    cd apps/api && uv sync --locked --no-install-project --no-dev

COPY apps/api/ ./apps/api/
COPY packages/shared/ ./packages/shared/

ENV PYTHONPATH=/app:/app/packages/shared
ENV PATH="/app/apps/api/.venv/bin:$PATH"

WORKDIR /app/apps/api
EXPOSE 5000

CMD ["python", "index.py"]
