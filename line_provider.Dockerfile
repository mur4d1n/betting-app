FROM python:3.10-slim as builder

WORKDIR /app

# Устанавливаем Poetry
RUN pip install --user --no-cache-dir poetry==1.7.0 alembic

# Копируем pyproject
COPY line_provider/pyproject.toml ./

# Устанавливаем зависимости
RUN python3 -m poetry config virtualenvs.create false && \
    python3 -m poetry install --no-interaction --no-ansi --only main

# Финальная стадия (минимизированный образ)
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install curl -y

# Копируем зависимости из билд-стадии
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Копируем код приложения
COPY line_provider/ ./line_provider/
COPY line_provider.alembic.ini ./alembic.ini

# Переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app:$PYTHONPATH

# Запуск приложения
CMD ["bash", "/app/line_provider/start.sh"]
