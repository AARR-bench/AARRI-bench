FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir pytest

WORKDIR /app

COPY lab_policy.md /app/lab_policy.md
COPY lab_meeting_notes/ /app/lab_meeting_notes/
COPY arxiv_alerts/ /app/arxiv_alerts/
COPY students/ /app/students/

RUN mkdir -p /app/feedback /logs/verifier
