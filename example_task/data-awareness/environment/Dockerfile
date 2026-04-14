FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY paper/main.tex /app/main.tex
