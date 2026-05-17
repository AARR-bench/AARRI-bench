FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pytest && \
    rm -rf /var/lib/apt/lists/*

COPY docs/project_brief.md /app/project_brief.md
COPY docs/input_spec.md /app/input_spec.md
COPY docs/backbone_note.md /app/backbone_note.md
COPY docs/modality_note.md /app/modality_note.md
COPY docs/ablation_log.md /app/ablation_log.md
COPY docs/engineering_pressure.md /app/engineering_pressure.md
COPY docs/module_1_input_packing.md /app/module_1_input_packing.md
COPY docs/module_2_interaction.md /app/module_2_interaction.md
COPY docs/module_3_pretrained_integration.md /app/module_3_pretrained_integration.md
COPY templates/constraint_audit_template.json /app/constraint_audit_template.json
COPY templates/module_review_template.json /app/module_review_template.json
COPY templates/final_design_template.json /app/final_design_template.json
