FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY tests/paper.txt .
COPY tests/context_paper1.txt .
COPY tests/context_paper2.txt .
