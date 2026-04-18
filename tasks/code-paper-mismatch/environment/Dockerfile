FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY proposal.md    /app/proposal.md
COPY appendix.tex   /app/appendix.tex
COPY train.py       /app/train.py
