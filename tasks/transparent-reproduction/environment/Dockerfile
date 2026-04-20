FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY artifacts/trace.json /app/trace.json
COPY artifacts/eval.py /app/eval.py
COPY artifacts/grade.py /app/grade.py
