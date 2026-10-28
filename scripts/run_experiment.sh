#!/usr/bin/env bash
# W2 - runs one script in a memory-limited container and reports how it ended
# and the peak memory of the whole container.
#
# Run from the repository root (the directory with src/ and data/):
#   ./scripts/run_experiment.sh mean-csv mean_csv.py 1280m
# Anything after the limit is passed to the script as its arguments:
#   ./scripts/run_experiment.sh rows-1000000 mean_rows.py 2g 1000000
#
# The script runs under `sh -c`. When the kernel kills python for exceeding the
# limit, the shell survives, so it can still print python's exit code and the
# container's memory.peak from its own cgroup. No host paths are involved, which
# is why this also works with Docker Desktop.
set -u
if [ $# -lt 3 ]; then
  echo "usage: $0 NAME SCRIPT LIMIT [ARGS...]   e.g. $0 mean-csv mean_csv.py 1280m"; exit 1
fi
name="$1" script="$2" limit="$3"
shift 3
if [ ! -d src ] || [ ! -d data ]; then
  echo "Run from the repository root - src/ and data/ not found in $PWD"; exit 1
fi
mkdir -p out
log="out/${name}-${limit}.log"

podman run --rm -m "$limit" --memory-swap "$limit" \
  -v "$PWD/data":/data -v "$PWD/src":/src -w /src oom-lab:1 \
  sh -c 'python "$0" "$@"; echo "exit=$?"; echo "peak=$(cat /sys/fs/cgroup/memory.peak)"' "$script" "$@" \
  > "$log" 2>&1

code=$(sed -n 's/^exit=//p' "$log")
peak=$(sed -n 's/^peak=//p' "$log")
case "$code" in
  0)   verdict=OK ;;
  137) verdict=ZABITY ;;
  *)   verdict="BLAD - zobacz $log" ;;
esac
printf '%-16s limit=%-7s exit=%-4s peak=%5d MB  %s\n' \
  "$name" "$limit" "${code:-?}" "$(( ${peak:-0} / 1000000 ))" "$verdict"
