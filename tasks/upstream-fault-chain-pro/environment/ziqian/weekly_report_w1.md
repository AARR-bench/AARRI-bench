# Weekly Report — Week 1
**Student:** Ziqian Meng
**Role:** Annotation QA & Data Pipeline
**Date:** 2025-01-03 to 2025-01-10

---

## Summary

This week was focused on setting up the annotation platform and running the initial pilot annotation batch. Primary activities included configuring the Labelbox instance, onboarding the annotator team, writing annotation guidelines, and conducting a quality assessment on the pilot run.

## Platform Setup

I deployed the annotation platform (Labelbox Enterprise) on our US West datacenter instance. Annotators access the platform via browser using credential-based login. The platform logs all session activity and records a server-local timestamp for each submitted annotation. I verified the export pipeline writes timestamps in ISO 8601 format without explicit timezone labeling — this is fine since all server-side operations run on the same datacenter clock.

I also set up the annotation filter pipeline (see `scripts/filter_work_hours.py`), which reads quality and timing parameters from `config/pipeline_config.yaml`. This ensures we only include annotations submitted during working hours.

## Pilot Annotation Run

Piloted with **50 dialogue pairs** drawn randomly from the MedDialogue corpus. All 18 annotators participated. Each pair was rated by 2 annotators independently.

**Inter-annotator agreement (IAA):** κ = 0.69

This is slightly below our target threshold of κ ≥ 0.70. After reviewing disagreements, I found that most arose from cases where one annotator prioritized clinical accuracy and the other prioritized tone/empathy. I updated the guidelines to clarify that both dimensions matter, weighted toward clinical safety first. I expect IAA to improve in the full run.

## Annotation Guidelines Update

Key clarifications added to the guidelines document:
- When both responses are clinically equivalent, prefer the one that is more patient-friendly in language
- Flag responses that recommend seeking emergency care — these are high-stakes and should always be preferred if appropriate
- Responses that use medication names without dosage should be rated lower for completeness

## Issues & Blockers

- One annotator (ANN007) submitted 12 annotations in rapid succession (~30 seconds apart), suggesting they may not have read the dialogues carefully. I temporarily suspended their account pending review.
- The export script initially failed on Unicode characters in a few dialogue texts. Fixed by enforcing UTF-8 encoding throughout the pipeline.

## Next Steps

- Launch full annotation run next week (target: 1,000+ pairs)
- Review IAA per-annotator to identify consistently low-agreement annotators
- Finalize quality filtering parameters in config
