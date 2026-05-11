"""
filter_work_hours.py
────────────────────
Filter raw annotation exports to retain only entries submitted during
annotator working hours, as defined in pipeline_config.yaml.

Usage:
    python filter_work_hours.py --input <raw_csv> --output <filtered_csv>
"""

import argparse
import csv
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).parent.parent / "config" / "pipeline_config.yaml"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def load_config(config_path: Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_timestamp(ts_str: str) -> datetime:
    """Parse a timestamp string in '%Y-%m-%d %H:%M:%S' format."""
    return datetime.strptime(ts_str.strip(), "%Y-%m-%d %H:%M:%S")


def is_within_work_hours(ts: datetime, start_hour: int, end_hour: int) -> bool:
    """Return True if the timestamp's hour falls within [start_hour, end_hour)."""
    return start_hour <= ts.hour < end_hour


def meets_quality_thresholds(row: dict, config: dict) -> bool:
    """Apply additional quality filters defined in config."""
    quality_cfg = config.get("quality", {})
    min_rating = quality_cfg.get("min_rating", 1)
    try:
        rating = int(row.get("rating", 0))
    except (ValueError, TypeError):
        return False
    return rating >= min_rating


def filter_annotations(
    input_path: Path,
    output_path: Path,
    config: dict,
) -> tuple[int, int]:
    """
    Read annotation CSV, apply work-hours and quality filters, write output CSV.
    Returns (n_input, n_output).
    """
    filter_cfg = config.get("annotation_filter", {})
    work_start = filter_cfg.get("work_hours_start", 9)
    work_end = filter_cfg.get("work_hours_end", 18)
    min_time_sec = filter_cfg.get("min_time_per_annotation_sec", 45)

    logger.info(
        "Work-hours filter: server hours %02d:00 – %02d:00", work_start, work_end
    )

    n_input = 0
    n_output = 0
    n_outside_hours = 0
    n_quality_fail = 0

    with open(input_path, "r", encoding="utf-8", newline="") as fin, open(
        output_path, "w", encoding="utf-8", newline=""
    ) as fout:
        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames or []
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            n_input += 1
            raw_ts = row.get("timestamp", "")
            try:
                ts = parse_timestamp(raw_ts)
            except ValueError:
                logger.warning("Could not parse timestamp '%s', skipping row.", raw_ts)
                n_quality_fail += 1
                continue

            if not is_within_work_hours(ts, work_start, work_end):
                n_outside_hours += 1
                if config.get("logging", {}).get("log_filter_decisions"):
                    logger.debug(
                        "EXCLUDED (outside hours): annotation_id=%s ts=%s hour=%d",
                        row.get("annotation_id"),
                        raw_ts,
                        ts.hour,
                    )
                continue

            if not meets_quality_thresholds(row, config):
                n_quality_fail += 1
                continue

            writer.writerow(row)
            n_output += 1

    logger.info(
        "Filter complete: %d input → %d retained (%d outside hours, %d quality fail)",
        n_input,
        n_output,
        n_outside_hours,
        n_quality_fail,
    )
    return n_input, n_output


def main():
    parser = argparse.ArgumentParser(description="Filter annotation CSV by work hours.")
    parser.add_argument("--input", required=True, help="Input annotation CSV path")
    parser.add_argument("--output", required=True, help="Output filtered CSV path")
    parser.add_argument(
        "--config", default=str(CONFIG_PATH), help="Path to pipeline_config.yaml"
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        logger.error("Config file not found: %s", config_path)
        sys.exit(1)

    config = load_config(config_path)
    logger.info("Loaded config from %s", config_path)

    n_in, n_out = filter_annotations(
        input_path=Path(args.input),
        output_path=Path(args.output),
        config=config,
    )

    retention_rate = (n_out / n_in * 100) if n_in > 0 else 0.0
    logger.info("Retention rate: %.1f%%", retention_rate)


if __name__ == "__main__":
    main()
