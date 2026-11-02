# monitor-alert-deduplicator

Collapse repeated monitoring alerts: same host and check inside a time window counts once, so alert storms become one actionable row.

## How to run

```sh
python3 main.py alerts.csv
```

## Example output

```
2026-10-31T09:00:00 h1 cpu: high load
Kept 1, dropped 2 duplicate(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
