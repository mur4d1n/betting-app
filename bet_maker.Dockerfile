FROM python:3.10-slim as builder

WORKDIR /app

# Устанавливаем Poetry
RUN pip install --user --no-cache-dir poetry==1.7.0 alembic

# Копируем только файлы зависимостей (для кэширования)
COPY bet_maker/pyproject.toml bet_maker/poetry.lock* ./

# Устанавливаем зависимости в системный Python (без создания виртуального окружения)
RUN python3 -m poetry config virtualenvs.create false && \
    python3 -m poetry install --no-interaction --no-ansi --only main

# === Финальная стадия (минимизированный образ) ===
FROM python:3.10-slim

WORKDIR /app

# Копируем зависимости из билд-стадии
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Копируем код приложения
COPY bet_maker/ ./bet_maker/
COPY alembic.ini ./

# Переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app:$PYTHONPATH

# Запуск приложения
CMD ["uvicorn", "bet_maker.main:app", "--host", "0.0.0.0", "--port", "8000"]
