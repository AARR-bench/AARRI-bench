FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY tests/mock_search.py .
