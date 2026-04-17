FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY paper/main.tex /app/paper.tex
COPY reviews/reviewer_a.txt /app/reviews/reviewer_a.txt
COPY reviews/reviewer_b.txt /app/reviews/reviewer_b.txt
