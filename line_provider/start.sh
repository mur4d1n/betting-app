#!/bin/bash

cd /app && alembic upgrade head
uvicorn line_provider.app:app --host 0.0.0.0 --port 8080
