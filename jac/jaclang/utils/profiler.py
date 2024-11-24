import time
from functools import wraps
from typing import Any, Callable, Dict


class CodeProfiler:

    markers: Dict[str, float] = {}

    @staticmethod
    def time_function(func: Callable):
        """Measure and print the execution time of a function."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            print(
                f"Function '{func.__name__}' took {end_time - start_time:.6f} seconds"
            )
            return result

        return wrapper

    @staticmethod
    def start_marker(marker_name: str) -> None:
        """Start a named marker to measure a specific section of code."""
        if marker_name in CodeProfiler.markers:
            print(f"Warning: Marker '{marker_name}' is already running.")
        CodeProfiler.markers[marker_name] = time.perf_counter()

    @staticmethod
    def end_marker(marker_name: str) -> None:
        """End the named marker and print the time taken since it started."""
        if marker_name not in CodeProfiler.markers:
            print(f"Error: Marker '{marker_name}' does not exist.")
            return
        start_time = CodeProfiler.markers.pop(marker_name)
        end_time = time.perf_counter()
        print(f"Marker '{marker_name}' took {end_time - start_time:.6f} seconds")
