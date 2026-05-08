FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/papers

COPY tests/main_paper.txt /app/papers/main_paper.txt
COPY tests/cited_paper.txt /app/papers/cited_paper.txt
