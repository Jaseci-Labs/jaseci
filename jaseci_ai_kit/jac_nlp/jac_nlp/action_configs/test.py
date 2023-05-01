import os
experiment="discussion_analysis"
payload = {
      "test": "synthetic_apps",
      "experiment": experiment,
      "mem": 4,
      "policy": "policy",
      "experiment_duration":300,
      "eval_phase":10,
      "perf_phase":100
}
f_name=f"{experiment}-{payload['mem']}.json"
if os.path.exists(f_name):
   print("yes")
else:
   print("no")