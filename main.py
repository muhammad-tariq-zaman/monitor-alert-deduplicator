"""Deduplicate monitoring alerts: same host + check within a window.

Usage: python3 main.py alerts.csv [--window-minutes 60]
CSV columns: timestamp,host,check,message (ISO timestamps).
Keeps the first alert per host+check per window and reports how many
duplicates were dropped.
"""
import argparse, csv, sys
from datetime import datetime, timedelta


def dedupe(rows, window_minutes):
    kept, dropped, last_seen = [], 0, {}
    for row in sorted(rows, key=lambda r: r["timestamp"]):
        key = (row["host"], row["check"])
        when = datetime.fromisoformat(row["timestamp"])
        if key in last_seen and when - last_seen[key] < timedelta(minutes=window_minutes):
            dropped += 1
            continue
        last_seen[key] = when
        kept.append(row)
    return kept, dropped


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--window-minutes", type=int, default=60)
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        kept, dropped = dedupe(list(csv.DictReader(f)), args.window_minutes)
    for row in kept:
        print(f"{row['timestamp']} {row['host']} {row['check']}: {row['message']}")
    print(f"Kept {len(kept)}, dropped {dropped} duplicate(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
