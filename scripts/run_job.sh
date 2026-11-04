#!/usr/bin/env bash
# W4 - runs one Hadoop Streaming job on the cluster and keeps the evidence in out/.
# Run it from the root of your repository, with the cluster up (compose-hdfs.yml + compose-yarn.yml).
#
#   ./scripts/run_job.sh NAME MAPPER REDUCER [COMBINER]
#   ./scripts/run_job.sh z1-mean mean_mapper.py mean_reducer.py
#
# The programs come from src/ (in the cluster: /src). Input: the HDFS directory /csv
# (another one with INPUT=/dir ./scripts/run_job.sh ...). Output in HDFS: /out/NAME.
# Kept here: out/NAME.log (everything the job printed) and out/NAME.tsv (the result).
set -euo pipefail

if [ $# -lt 3 ]; then
  echo "usage: $0 NAME MAPPER REDUCER [COMBINER]" >&2
  exit 2
fi
name=$1 mapper=$2 reducer=$3 combiner=${4:-}
input=${INPUT:-/csv}
nn="podman-compose -f compose-hdfs.yml -f compose-yarn.yml exec -T namenode"
mkdir -p out

# The same options as in the word count demo; -files copies the programs to every node that gets a task.
files="/src/$mapper,/src/$reducer"
opts=(-mapper "python3 $mapper" -reducer "python3 $reducer")
if [ -n "$combiner" ]; then
  files="$files,/src/$combiner"
  opts+=(-combiner "python3 $combiner")
fi

# Right after `up` the NameNode is in safe mode (it collects block reports) and refuses writes.
until $nn hdfs dfsadmin -safemode get 2>/dev/null | grep -q OFF; do
  echo "waiting for HDFS to leave safe mode..."
  sleep 3
done

# Hadoop refuses to write into an existing output directory, so a re-run starts by removing it.
$nn hdfs dfs -rm -r -f -skipTrash "/out/$name" > /dev/null

t0=$(date +%s%N)
# -D sets the job name shown on localhost:8088; generic options must come first
if ! $nn mapred streaming -D mapreduce.job.name="$name" -files "$files" "${opts[@]}" \
     -input "$input" -output "/out/$name" > "out/$name.log" 2>&1; then
  grep -E 'ERROR|Error|failed' "out/$name.log" | tail -5
  app=$(grep -o 'application_[0-9_]*' "out/$name.log" | head -1)
  echo "JOB FAILED. Full log: out/$name.log"
  # task logs reach HDFS a few seconds after the job ends; if this prints nothing, run it again
  [ -n "$app" ] && echo "Python traceback: podman compose -f compose-hdfs.yml exec -T namenode yarn logs -applicationId $app -log_files stderr | grep -A 5 Traceback"
  exit 1
fi
t1=$(date +%s%N)
$nn hdfs dfs -cat "/out/$name/part-*" > "out/$name.tsv"

grep -E 'Submitted application|Launched map tasks|Data-local map tasks|Launched reduce tasks|Map input records|Map output records|Combine input records|Combine output records|Reduce input records|Reduce shuffle bytes|Reduce output records' \
  "out/$name.log" | sed -E 's/^.*(Submitted application)/\1/; s/^[[:space:]]+//'
awk -v ms=$(( (t1 - t0) / 1000000 )) -v f="out/$name.tsv" -v n="$(wc -l < "out/$name.tsv")" \
  'BEGIN { printf "time: %.1f s   result: %s (%d lines)\n", ms / 1000, f, n }'
