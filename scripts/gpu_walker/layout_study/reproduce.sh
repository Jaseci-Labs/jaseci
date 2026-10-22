#!/usr/bin/env bash
# Run from the repository root with a fresh validation destination.
set -euo pipefail
study_out=${1:?Usage: reproduce.sh scripts/gpu_walker/layout_study/validation/NEW_RUN}
study_source=scripts/gpu_walker/layout_study
mkdir -p "$study_out"
env/bin/python "$study_source/prepare.py" --output "$study_out/inputs"
PYTHONPATH=jac:scripts/gpu_walker env/bin/python "$study_source/emit_checked_o2.py" --inputs "$study_out/inputs/inputs.json" --output "$study_out/optimized-codegen" > "$study_out/optimized-codegen.log" 2>&1
mkdir -p "$study_out/optimized-profile"
/usr/local/bin/nsys profile --trace=cuda --cuda-graph-trace=node --sample=none --cpuctxsw=none --output "$study_out/optimized-profile/trace" env/bin/python "$study_source/run.py" --inputs "$study_out/inputs/inputs.json" --jac-ptx "$study_out/optimized-codegen/O2.ptx" --output "$study_out/optimized-profile" --warmup 3 --repeats 15 > "$study_out/optimized-profile/run.log" 2>&1
/usr/local/bin/nsys export --type sqlite --output "$study_out/optimized-profile/trace.sqlite" "$study_out/optimized-profile/trace.nsys-rep"
env/bin/python "$study_source/analyze.py" "$study_out/optimized-profile/results.json" "$study_out/optimized-profile/trace.sqlite" --output "$study_out/optimized-profile/verified.json"
env/bin/python "$study_source/run.py" --inputs "$study_out/inputs/inputs.json" --jac-ptx "$study_out/optimized-codegen/O2.ptx" --output "$study_out/optimized-ordinary" > "$study_out/optimized-ordinary.log" 2>&1
env/bin/python "$study_source/address_analysis.py" --inputs "$study_out/inputs/inputs.json" --profile "$study_out/optimized-profile/results.json" --output "$study_out/optimized-address-analysis.json"
env/bin/python "$study_source/counter_probe.py" "$study_out"
env/bin/python "$study_source/build_report.py" "$study_out"
