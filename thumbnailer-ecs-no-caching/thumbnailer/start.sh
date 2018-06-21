#!/bin/bash
echo Starting Gunicorn...
gunicorn --bind=0.0.0.0:8000 \
         --workers=3 --worker-class=gevent \
         --access-logfile '-' --error-logfile '-' --capture-output \
         thumbnailer.wsgi
