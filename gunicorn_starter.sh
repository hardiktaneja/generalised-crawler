#!/bin/bash
gunicorn -w 1 --threads=15 --reload -b 0.0.0.0:5000 "app.main:create_app('dev')" --limit-request-line 81900

