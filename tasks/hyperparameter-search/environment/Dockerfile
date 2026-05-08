FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY tests/train.py /app/train.py
