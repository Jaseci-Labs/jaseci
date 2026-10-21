#!/usr/bin/env bash
# Run from any directory. Uses an isolated output directory and saved real inputs.
set -euo pipefail
cd "$(dirname "$0")/../../.."
task_source=scripts/gpu_walker/handwritten_matmul
task_output=${1:-/tmp/jac-matmul-codegen-reproduction}
if [[ -e "$task_output/codegen" ]]; then
    printf 'Refusing to overwrite an existing codegen directory: %s\n' "$task_output/codegen" >&2
    exit 1
fi
mkdir -p "$task_output/codegen/paired-ordinary" "$task_output/codegen/paired-profile" "$task_output/codegen/ablation-ordinary" "$task_output/codegen/ablation-profile"
cp -a "$task_source/validation/20261021/inputs" "$task_output/"
cp "$task_source/validation/20261021/DENSE_BASELINES.md" "$task_output/"
cp "$task_source/benchmark.py" "$task_output/codegen/paired-benchmark.py"
cp "$task_source/analyze_profile.py" "$task_output/codegen/paired-analyze_profile.py"
export PYTHONPATH=jac:scripts/gpu_walker
run() {
    printf '%q ' "$@" >> "$task_output/codegen/commands.txt"
    printf '\n' >> "$task_output/codegen/commands.txt"
    "$@"
}
run env/bin/python "$task_source/diagnose_codegen.py" --output "$task_output/codegen" --baseline-ptx "$task_output/inputs/Dot.ptx" > "$task_output/codegen/build.log" 2>&1
paired=(--inputs "$task_output/inputs/inputs.json" --jac-variant "O2=$task_output/codegen/O2.ptx")
extra=(--jac-variant "hoist_sroa=$task_output/codegen/hoist_sroa.ptx" --jac-variant "O2_no_overflow=$task_output/codegen/O2_no_overflow.ptx" --jac-variant "O2_no_validation=$task_output/codegen/O2_no_validation.ptx" --jac-variant "O2_unchecked=$task_output/codegen/O2_unchecked.ptx" --graph-controls)
run env/bin/python "$task_source/benchmark.py" "${paired[@]}" --output "$task_output/codegen/paired-ordinary" > "$task_output/codegen/paired-ordinary/run.log" 2>&1
run /usr/local/bin/nsys profile --trace=cuda --cuda-graph-trace=node --sample=none --cpuctxsw=none --force-overwrite=true --output "$task_output/codegen/paired-profile/trace" env/bin/python "$task_source/benchmark.py" "${paired[@]}" --output "$task_output/codegen/paired-profile" --warmup 3 --repeats 15 > "$task_output/codegen/paired-profile/run.log" 2>&1
run env/bin/python "$task_source/benchmark.py" "${paired[@]}" "${extra[@]}" --output "$task_output/codegen/ablation-ordinary" > "$task_output/codegen/ablation-ordinary/run.log" 2>&1
run /usr/local/bin/nsys profile --trace=cuda --cuda-graph-trace=node --sample=none --cpuctxsw=none --force-overwrite=true --output "$task_output/codegen/ablation-profile/trace" env/bin/python "$task_source/benchmark.py" "${paired[@]}" "${extra[@]}" --output "$task_output/codegen/ablation-profile" --warmup 3 --repeats 15 > "$task_output/codegen/ablation-profile/run.log" 2>&1
for task_run in paired-profile ablation-profile; do
    run /usr/local/bin/nsys export --type sqlite --force-overwrite=true --output "$task_output/codegen/$task_run/trace.sqlite" "$task_output/codegen/$task_run/trace.nsys-rep" > "$task_output/codegen/$task_run/export.log" 2>&1
    run env/bin/python "$task_source/analyze_profile.py" "$task_output/codegen/$task_run/results.json" "$task_output/codegen/$task_run/trace.sqlite" --output "$task_output/codegen/$task_run/verified-kernels.json"
done
run env/bin/python "$task_source/validate_codegen.py" --codegen "$task_output/codegen" --output "$task_output/codegen/status-validation.json" > "$task_output/codegen/status-validation.log" 2>&1
run env/bin/python -m unittest discover -s scripts/gpu_walker -p test_named_cursors.py -v > "$task_output/codegen/named-cursors-cpu-jit.log" 2>&1
run env/bin/python "$task_source/build_diagnosis_report.py" "$task_output"
