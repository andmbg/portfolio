#!/bin/bash
exec gunicorn --workers 3 --bind 0.0.0.0:8080 wsgi:flask_app
