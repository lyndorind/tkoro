#!/usr/bin/env bash
set -euo pipefail

mkdir -p reports/jmeter
api_container=lab7-load-api
db_container=$(docker ps --quiet --filter 'ancestor=postgres:16-bookworm' | head -n 1)

if [[ -z "$db_container" ]]; then
  echo 'PostgreSQL service container was not found' >&2
  exit 1
fi

printf 'timestamp,container,cpu,memory,memory_percent\n' > reports/jmeter/docker-stats.csv

(
  while true; do
    timestamp=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    docker stats --no-stream --format '{{.Name}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}}' \
      "$api_container" "$db_container" | while IFS= read -r sample; do
      printf '%s,%s\n' "$timestamp" "$sample"
    done >> reports/jmeter/docker-stats.csv
    sleep 2
  done
) &
monitor_pid=$!

function stop_monitor {
  kill "$monitor_pid" 2>/dev/null || true
  wait "$monitor_pid" 2>/dev/null || true
}
trap stop_monitor EXIT

"${JMETER_BIN:-jmeter}" -n \
  -t jmeter/lab7.jmx \
  -l reports/jmeter/results.jtl \
  -j reports/jmeter/jmeter.log \
  -e -o reports/jmeter/html \
  -Jhost=127.0.0.1 -Jport=8000

python3 - <<'PY'
import csv
from pathlib import Path

results_path = Path("reports/jmeter/results.jtl")
with results_path.open(encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

if not rows:
    raise SystemExit("JMeter returned zero samples")

failed = [row for row in rows if row.get("success", "").lower() != "true"]
print(f"JMeter samples: {len(rows)}, failed: {len(failed)}")
if failed:
    for sample in failed[:5]:
        print(sample.get("label"), sample.get("responseCode"), sample.get("responseMessage"))
    raise SystemExit("JMeter reported failed HTTP samples")
PY
