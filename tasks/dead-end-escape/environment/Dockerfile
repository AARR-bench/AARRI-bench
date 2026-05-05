FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 && \
    rm -rf /var/lib/apt/lists/*

COPY docs/current_hypothesis.md /app/current_hypothesis.md
COPY docs/attempt_history.md /app/attempt_history.md
COPY docs/global_constraints.md /app/global_constraints.md
COPY docs/lab_meeting_notes.md /app/lab_meeting_notes.md
COPY failure_logs /app/failure_logs
COPY templates/dead_end_audit_template.json /app/dead_end_audit_template.json
