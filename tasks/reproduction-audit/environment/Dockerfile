FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY artifacts/eval_coco.py /app/eval_coco.py
COPY artifacts/run_log.txt /app/run_log.txt
