"""Built in actions for Jaseci"""
from jaseci.jsorc.live_actions import jaseci_action
from jaseci.utils.utils import perf_test_start, perf_test_stop

perf_tests = {}


@jaseci_action()
def start_perf_test(name: str = "default"):
    perf_tests[name] = perf_test_start()


@jaseci_action()
def stop_perf_test(name: str = "default"):
    if name not in perf_tests.keys():
        return
    calls, graph = perf_test_stop(perf_tests[name])
    return {"calls": calls, "graph": graph}
