FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY tests/paper_draft.txt .
COPY tests/reviewer_comments.txt .
