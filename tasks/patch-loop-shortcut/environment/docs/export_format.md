# Export Format

Each CSV begins with lightweight comment metadata followed by tabular rows.

Relevant fields:

- `run_id`
- `time_unit`
- `time`
- `signal`

The exporting software keeps the native acquisition unit in the `time` column and records that unit in the metadata header.

Examples of valid units in this project:

- `s`
- `ms`

Downstream tools are expected to interpret the raw time axis using the recorded metadata before applying fixed analysis rules.
