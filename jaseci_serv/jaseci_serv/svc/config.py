import sys

RUN_SVCS = (
    "test" in sys.argv
    or "runserver" in sys.argv
    or any(["pytest" in arg for arg in sys.argv])
)
