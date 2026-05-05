FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl python3 coreutils && \
    rm -rf /var/lib/apt/lists/*

COPY README.md download.sh train.py ./
RUN chmod +x download.sh