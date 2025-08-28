
FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright (optional, comment out if not needed initially)
RUN pip install --no-cache-dir playwright && playwright install --with-deps chromium

COPY . .
