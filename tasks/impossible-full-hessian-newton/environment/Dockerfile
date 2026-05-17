FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates python3 python3-pytest \
    && rm -rf /var/lib/apt/lists/*

COPY proposal.md /app/proposal.md
