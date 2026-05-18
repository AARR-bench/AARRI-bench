FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY artifacts/problem.md /app/problem.md
COPY artifacts/categories.json /app/categories.json
COPY artifacts/consult.py /app/consult.py
