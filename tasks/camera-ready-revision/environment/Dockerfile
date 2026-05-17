FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest --break-system-packages

COPY paper/main.tex /app/paper.tex
COPY reviews/reviewer_a.txt /app/reviews/reviewer_a.txt
COPY reviews/reviewer_b.txt /app/reviews/reviewer_b.txt
