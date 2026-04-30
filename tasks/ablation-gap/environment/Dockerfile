FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pytest && \
    rm -rf /var/lib/apt/lists/*