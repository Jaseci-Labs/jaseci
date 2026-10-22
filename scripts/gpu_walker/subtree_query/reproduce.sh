#!/usr/bin/env bash
# Rebuild complete subtree evidence in a fresh output directory; GPU access required.
set -euo pipefail
cd "$(dirname "$0")/../../.."
task_source=scripts/gpu_walker/subtree_query
task_output=${1:-/tmp/jac-subtree-reproduction}
if [[ -e "$task_output/inputs.json" ]]; then
    printf 'Choose a fresh output directory: %s\n' "$task_output" >&2
    exit 1
fi
mkdir -p "$task_output" "$task_output/profile" "$task_output/ablation-ordinary" "$task_output/ablation-profile"
export PYTHONPATH=jac:scripts/gpu_walker
run() {
    printf '%q ' "$@" >> "$task_output/commands.txt"
    printf '\n' >> "$task_output/commands.txt"
    "$@"
}
run env/bin/python "$task_source/common.py" --probe "$task_output/memory-probe.json"
run env/bin/python "$task_source/prepare.py" --output "$task_output" --memory-probe "$task_output/memory-probe.json" > "$task_output/prepare.log" 2>&1
run env/bin/python "$task_source/run.py" --inputs "$task_output/inputs.json" --output "$task_output/ordinary" > "$task_output/ordinary.log" 2>&1
run /usr/local/bin/nsys profile --trace=cuda --cuda-graph-trace=node --sample=none --cpuctxsw=none --force-overwrite=true --output "$task_output/profile/trace" env/bin/python "$task_source/run.py" --inputs "$task_output/inputs.json" --output "$task_output/profile" --warmup 3 --repeats 15 > "$task_output/profile/run.log" 2>&1
run env/bin/python "$task_source/run.py" --inputs "$task_output/inputs.json" --output "$task_output/ablation-ordinary" --ablations --warmup 3 --repeats 15 > "$task_output/ablation-ordinary/run.log" 2>&1
run /usr/local/bin/nsys profile --trace=cuda --cuda-graph-trace=node --sample=none --cpuctxsw=none --force-overwrite=true --output "$task_output/ablation-profile/trace" env/bin/python "$task_source/run.py" --inputs "$task_output/inputs.json" --output "$task_output/ablation-profile" --ablations --warmup 3 --repeats 15 > "$task_output/ablation-profile/run.log" 2>&1
run env/bin/python "$task_source/validate.py" --validation "$task_output" > "$task_output/correctness.log" 2>&1
for task_run in profile ablation-profile; do
    run /usr/local/bin/nsys export --type sqlite --force-overwrite=true --output "$task_output/$task_run/trace.sqlite" "$task_output/$task_run/trace.nsys-rep" > "$task_output/$task_run/export.log" 2>&1
    run env/bin/python "$task_source/analyze.py" "$task_output/$task_run/results.json" "$task_output/$task_run/trace.sqlite" --output "$task_output/$task_run/verified.json"
done
run env/bin/python -m unittest discover -s scripts/gpu_walker -p test_subtree.py -v > "$task_output/existing-subtree-cpu.log" 2>&1
run env/bin/python "$task_source/build_report.py" "$task_output"
run env/bin/python "$task_source/record_provenance.py" "$task_output"
printf 'PDF deck source: docs/presentations/jac-gpu-subtree/generate.py\n'
