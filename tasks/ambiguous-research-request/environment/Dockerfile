FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 && \
    rm -rf /var/lib/apt/lists/*

COPY docs/user_request.md /app/user_request.md
COPY docs/project_context.md /app/project_context.md
COPY docs/constraints.md /app/constraints.md
COPY docs/existing_workflow.md /app/existing_workflow.md
COPY docs/stakeholder_notes.md /app/stakeholder_notes.md
COPY templates/decision_questions_template.json /app/decision_questions_template.json
COPY templates/option_space_template.json /app/option_space_template.json
