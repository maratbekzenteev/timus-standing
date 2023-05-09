#!/bin/sh

# WSGI and 10 minute update coroutine startup script

python ./coroutines.py &
gunicorn --bind 0.0.0.0:5000 wsgi:app

