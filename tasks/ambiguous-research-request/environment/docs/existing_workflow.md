# Existing Workflow

The team currently copies experiment rows into a spreadsheet.

Common failure modes:

- People sort by the target mIoU column and ignore whether the result is reproducible.
- Failed runs are sometimes omitted without being marked.
- One-seed runs get compared with three-seed runs.
- Some people want a paper-facing story; others want to know what broke.
- Negative results are sometimes described as "method failed" before the pipeline or objective has been isolated.
