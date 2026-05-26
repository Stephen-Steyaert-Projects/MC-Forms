FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project


FROM ghcr.io/astral-sh/uv:python3.13-alpine AS runner

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

RUN addgroup -S appgroup && adduser -S -G appgroup -s /sbin/nologin appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --chown=appuser:appgroup . .

RUN mkdir -p /app/staticfiles /app/database && chown -R appuser:appgroup /app/staticfiles /app/database

RUN chmod +x /app/entrypoint.prod.sh

USER appuser

EXPOSE 8000

CMD ["./entrypoint.prod.sh"]
