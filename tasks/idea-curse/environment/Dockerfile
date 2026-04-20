FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY artifacts/problem.md /app/problem.md
COPY artifacts/categories.json /app/categories.json
COPY artifacts/consult.py /app/consult.py
