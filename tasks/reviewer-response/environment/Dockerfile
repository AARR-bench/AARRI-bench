FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir --break-system-packages pytest==8.4.1 pytest-json-ctrf==0.3.5 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY paper_draft.txt /app/paper_draft.txt
COPY reviewer_comments.txt /app/reviewer_comments.txt
