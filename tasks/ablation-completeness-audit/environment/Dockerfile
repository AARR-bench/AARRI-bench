FROM ubuntu:24.04
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip curl ca-certificates && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/logs /app/paper

COPY generate_logs.py /tmp/generate_logs.py
RUN python3 /tmp/generate_logs.py && rm /tmp/generate_logs.py

COPY paper_excerpt.txt /app/paper/excerpt.txt
