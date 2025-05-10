FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

FROM python:3.12-slim

COPY --from=builder --chown=app:app /app/.venv /app/.venv

COPY helpers/ /app/helpers/
COPY jobs/ /app/jobs/

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

CMD ["sh", "-c", "rq worker --with-scheduler --url redis://$REDIS_HOST:$REDIS_PORT $QUEUE"]