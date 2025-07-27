#!/bin/sh

# The virtual environment is already activated through ENV PATH in Dockerfile
# Just run gunicorn
gunicorn --bind 0.0.0.0:8000 --workers=3 --timeout 90 run:app