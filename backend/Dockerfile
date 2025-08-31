# Base
FROM python:3.13-slim AS base
WORKDIR /app

ARG USER_UID=1000

RUN apt-get update && apt-get upgrade -y \
  && rm -rf /var/lib/apt/lists/*

RUN groupadd -g $USER_UID user \
  && useradd -rm -u $USER_UID -g user user \
  && chown -R user:user /app

USER user

# Builder
FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY --chown=user:user pyproject.toml uv.lock ./
RUN uv sync --no-install-project --no-dev

COPY --chown=user:user src ./src
RUN uv sync --no-dev

# Runner
FROM base AS runner

ENV PATH="/app/.venv/bin:$PATH"
COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/src ./src

CMD [ "fastapi", "run", "src/backend/main.py" ]
