#!/bin/bash

pip install $MODULE_NAME
export PYTHONPATH=/app
python server/server.py $MODULE_NAME
