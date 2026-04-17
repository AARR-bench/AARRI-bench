FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY paper/main.tex /app/paper.tex
COPY reviews/reviewer_1.txt /app/reviews/reviewer_1.txt
COPY reviews/reviewer_2.txt /app/reviews/reviewer_2.txt
COPY reviews/reviewer_3.txt /app/reviews/reviewer_3.txt
