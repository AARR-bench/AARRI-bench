FROM ubuntu:24.04
WORKDIR /app

RUN apt-get update && apt-get install -y python3 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/runs

COPY generate_logs.py /tmp/generate_logs.py
RUN python3 /tmp/generate_logs.py && rm /tmp/generate_logs.py
