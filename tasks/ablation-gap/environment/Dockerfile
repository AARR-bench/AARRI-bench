FROM ubuntu:24.04

WORKDIR /app

RUN sed -i 's|http://ports.ubuntu.com|http://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list.d/ubuntu.sources && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pytest curl && \
    rm -rf /var/lib/apt/lists/*