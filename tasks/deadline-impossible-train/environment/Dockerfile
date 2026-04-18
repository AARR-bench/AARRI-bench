FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY proposal.md /app/proposal.md
COPY train_config.yaml /app/train_config.yaml
