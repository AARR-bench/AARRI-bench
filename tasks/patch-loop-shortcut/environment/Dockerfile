FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pytest && \
    rm -rf /var/lib/apt/lists/*

COPY src/analyze.py /app/analyze.py
COPY docs/analysis_goal.md /app/analysis_goal.md
COPY docs/export_format.md /app/export_format.md
COPY notes/attempt_history.md /app/attempt_history.md
COPY data/run_a.csv /app/data/run_a.csv
COPY data/run_b.csv /app/data/run_b.csv
COPY data/run_c.csv /app/data/run_c.csv
COPY templates/symptom_audit_template.json /app/symptom_audit_template.json
COPY templates/repair_strategy_template.json /app/repair_strategy_template.json
