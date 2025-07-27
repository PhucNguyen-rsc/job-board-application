#!/bin/bash

export FLASK_ENV=development
export PROJ_DIR=$PWD
export DEBUG=1

# run our server locally:
FLASK_APP=run.py flask run --debug --host=127.0.0.1 --port=8000
