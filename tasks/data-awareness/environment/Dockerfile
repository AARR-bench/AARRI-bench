FROM ubuntu:24.04

WORKDIR /app

RUN sed -i 's|http://ports.ubuntu.com|http://mirrors.aliyun.com|g' /etc/apt/sources.list.d/ubuntu.sources && \
    apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY paper/main.tex /app/main.tex
