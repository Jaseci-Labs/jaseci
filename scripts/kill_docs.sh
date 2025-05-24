#!/bin/bash
# Script to find and kill processes listening on a specific port (e.g., 8000 for docs)
# and verify they are terminated.

PORT_TO_KILL=8000

# Find PIDs listening on the specified port
PIDS=$(lsof -i :${PORT_TO_KILL} -t 2>/dev/null)

if [ -z "$PIDS" ]; then
    echo "No process found listening on port ${PORT_TO_KILL}."
    exit 0
fi

echo "Found the following PIDs on port ${PORT_TO_KILL}: $PIDS"
echo "Attempting to kill them with SIGKILL (kill -9)..."

# Kill the processes
# The `2>/dev/null` suppresses errors if a PID in the list has already exited
# xargs -r (or --no-run-if-empty) ensures kill is not run if PIDS is empty (though we check above)
echo "$PIDS" | xargs -r --no-run-if-empty kill -9 2>/dev/null

# Wait a moment for processes to terminate
sleep 1

# Verify that the processes are killed
STILL_ALIVE_PIDS=$(lsof -i :${PORT_TO_KILL} -t 2>/dev/null)

if [ -z "$STILL_ALIVE_PIDS" ]; then
    echo "Successfully killed all processes on port ${PORT_TO_KILL}."
    exit 0
else
    echo "ERROR: The following PIDs on port ${PORT_TO_KILL} might still be alive: $STILL_ALIVE_PIDS"
    echo "Please check manually or investigate if they are being respawned by a supervisor."
    exit 1
fi