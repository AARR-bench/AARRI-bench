FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install pytest pytest-json-ctrf --break-system-packages

COPY artifacts/eval_coco.py /app/eval_coco.py
COPY artifacts/run_log.txt /app/run_log.txt
