FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl python3 python3-pytest && \
    rm -rf /var/lib/apt/lists/*

COPY paper/paper.tex /app/paper/paper.tex
COPY code/run_eval.py /app/code/run_eval.py