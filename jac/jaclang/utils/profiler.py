import time
from contextlib import contextmanager
from functools import wraps
from typing import Callable, Dict, Generator, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


class CodeProfiler:

    markers: Dict[str, float] = {}

    @staticmethod
    def time_function(func: Callable[P, R]) -> Callable[P, R]:
        """Measure and print the execution time of a function."""

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
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

    @staticmethod
    @contextmanager
    def profile_section(section_name: str) -> Generator[None, None, None]:
        """
        A context manager for profiling a block of code.

        Usage:
            with CodeProfiler.profile_section("My Block"):
                # code to profile
        """
        start_time = time.perf_counter()
        try:
            yield
        finally:
            end_time = time.perf_counter()
            print(f"Section '{section_name}' took {end_time - start_time:.6f} seconds")
