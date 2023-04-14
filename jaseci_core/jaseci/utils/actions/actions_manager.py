from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.prome_svc import PrometheusService
from jaseci.jsorc.live_actions import load_action_config
from .actions_optimizer import ActionsOptimizer

import time
import numpy as np


@JsOrc.context("action_manager")
class ActionManager:
    def __init__(self):
        self.benchmark = {
            "jsorc": {"active": False, "requests": {}},
            "actions_optimizer": {"active": False, "requests": {}},
        }
        self.actions_history = {"active": False, "history": []}
        self.actions_calls = {}
        self.system_states = {"active": False, "states": []}
        self.actions_optimizer = ActionsOptimizer(
            benchmark=self.benchmark["actions_optimizer"],
            actions_history=self.actions_history,
            actions_calls=self.actions_calls,
        )

    ###################################################
    #                 ACTION MANAGER                  #
    ###################################################

    def load_action_config(self, config, name):
        """
        Load the config for an action
        """
        return load_action_config(config, name)

    def load_actions(self, name, mode):
        """
        Load an action as local, module or remote.
        """
        # Using module for local
        mode = "module" if mode == "local" else mode

        if mode == "module":
            self.actions_optimizer.load_action_module(name)
        elif mode == "remote":
            self.actions_optimizer.load_action_remote(name)

    def unload_actions(self, name, mode, retire_svc):
        """
        Unload an action
        """
        # We are using module for local
        mode = "module" if mode == "local" else mode
        if mode == "auto":
            res = self.actions_optimizer.unload_action_auto(name)
            if not res[0]:
                return res
            if retire_svc:
                self.retire_uservice(name)
            return res
        elif mode == "module":
            return self.actions_optimizer.unload_action_module(name)
        elif mode == "remote":
            res = self.actions_optimizer.unload_action_remote(name)
            if not res[0]:
                return res
            if retire_svc:
                self.retire_uservice(name)
            return res
        else:
            return (False, f"Unrecognized action mode {mode}.")

    def retire_uservice(self, name):
        """
        Retire a remote microservice for the action.
        """
        self.actions_optimizer.retire_remote(name)

    def get_actions_status(self, name=""):
        """
        Return the status of the action
        """
        return self.actions_optimizer.get_actions_status(name)

    def actions_tracking_start(self):
        """ """
        self.actions_history["active"] = True
        self.actions_history["history"] = [{"ts": time.time()}]
        self.actions_calls.clear()

    def actions_tracking_stop(self):
        """ """
        if not self.actions_history["active"]:
            return []

        self.actions_optimizer.summarize_action_calls()

        return self.actions_history["history"]

    def benchmark_start(self):
        """
        Put JSORC under benchmark mode.
        """
        self.benchmark["jsorc"]["active"] = True
        self.benchmark["jsorc"]["requests"] = {}
        self.benchmark["jsorc"]["start_ts"] = time.time()

    def state_tracking_start(self):
        """
        Ask JSORC to start tracking the state of the system as observed by JSORC on every interval.
        """
        self.system_states = {"active": True, "states": []}

    def state_tracking_stop(self):
        """
        Stop state tracking for JSORC
        """
        ret = self.system_states
        self.system_states = {"active": True, "states": []}
        return ret

    def state_tracking_report(self):
        """
        Return state tracking history so far
        """
        return self.system_states

    def record_system_state(self):
        """
        Record system state
        """
        if self.system_states["active"]:
            ts = int(time.time())
            prom_profile = (
                JsOrc.svc("prome")
                .poke(PrometheusService)
                .info(
                    namespace=self.namespace,
                    exclude_prom=True,
                    timestamp=ts,
                    duration=self.backoff_interval,
                )
            )
            self.system_states["states"].append(
                {
                    "ts": ts,
                    "actions": self.get_actions_status(name=""),
                    "prometheus": prom_profile,
                }
            )

    def benchmark_stop(self, report):
        """
        Stop benchmark mode and report result during the benchmark period
        """
        if not self.benchmark["jsorc"]["active"]:
            return {}

        res = self.benchmark_report()
        self.benchmark["jsorc"]["requests"] = {}
        self.benchmark["jsorc"]["active"] = False

        if report:
            return res
        else:
            return {}

    def benchmark_report(self):
        """
        Summarize benchmark results and report.
        """
        summary = {}
        duration = time.time() - self.benchmark["jsorc"]["start_ts"]
        for request, data in self.benchmark["jsorc"]["requests"].items():
            summary[request] = {}
            all_reqs = []
            for req_name, times in data.items():
                if len(times) == 0:
                    continue
                all_reqs.extend(times)
                summary[request][req_name] = {
                    "throughput": len(times) / duration,
                    "average_latency": sum(times) / len(times) * 1000,
                    "50th_latency": np.percentile(times, 50) * 1000,
                    "90th_latency": np.percentile(times, 90) * 1000,
                    "95th_latency": np.percentile(times, 95) * 1000,
                    "99th_latency": np.percentile(times, 99) * 1000,
                }
            summary[request]["all"] = {
                "throughput": len(all_reqs) / duration,
                "average_latency": sum(all_reqs) / len(all_reqs) * 1000,
                "50th_latency": np.percentile(all_reqs, 50) * 1000,
                "90th_latency": np.percentile(all_reqs, 90) * 1000,
                "95th_latency": np.percentile(all_reqs, 95) * 1000,
                "99th_latency": np.percentile(all_reqs, 99) * 1000,
            }

        return summary

    def record_state(self):
        """
        Record the current state of the system observed by JSORC
        """

    def add_to_benchmark(self, request_type, request, request_time):
        """
        Add requests to benchmark performance tracking
        """
        for bm in self.benchmark.values():
            if request_type not in bm["requests"]:
                bm["requests"][request_type] = {"_default_": []}
            if request_type == "walker_run":
                walker_name = dict(request.data)["name"]
                if walker_name not in bm["requests"][request_type]:
                    bm["requests"][request_type][walker_name] = []
                bm["requests"][request_type][walker_name].append(request_time)
            else:
                bm["requests"][request_type]["_default_"].append(request_time)

    def set_action_policy(self, policy_name, policy_params):
        """
        Set an action optimizer policy
        """
        return self.actions_optimizer.set_action_policy(policy_name, policy_params)

    def get_action_policy(self):
        """
        Get the current action optimization policy
        """
        return self.actions_optimizer.get_action_policy()

    def pre_action_call_hook(self, *args):
        pass

    def post_action_call_hook(self, *args):
        action_name = args[0]
        action_time = args[1]
        if action_name not in self.actions_calls:
            self.actions_calls[action_name] = []

        self.actions_calls[action_name].append(action_time)

    def pre_request_hook(self, *args):
        pass

    def post_request_hook(self, *args):
        request_type = args[0]
        request = args[1]
        request_time = args[2]
        if self.benchmark["jsorc"]["active"]:
            self.add_to_benchmark(request_type, request, request_time)

    def optimize(self, jsorc_interval):
        self.actions_optimizer.run(jsorc_interval)
