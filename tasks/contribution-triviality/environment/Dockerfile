FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY tests/paper.txt /app/paper.txt
COPY tests/context_paper1.txt /app/context_paper1.txt
COPY tests/context_paper2.txt /app/context_paper2.txt
