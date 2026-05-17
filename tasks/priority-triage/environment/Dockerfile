FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir pytest

WORKDIR /app

COPY requests/ /app/requests/

RUN mkdir -p /app/responses /logs/verifier
