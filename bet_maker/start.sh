#!/bin/bash

cd /app && alembic upgrade head
uvicorn bet_maker.main:app --host 0.0.0.0 --port 8000
