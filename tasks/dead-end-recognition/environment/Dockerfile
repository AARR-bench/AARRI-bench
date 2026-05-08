FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/logs

COPY tests/run1.txt /app/logs/run1.txt
COPY tests/run2.txt /app/logs/run2.txt
COPY tests/run3.txt /app/logs/run3.txt
COPY tests/run4.txt /app/logs/run4.txt
COPY tests/run5.txt /app/logs/run5.txt
