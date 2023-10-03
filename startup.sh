#!/bin/bash
python manage.py ingest_data && python manage.py analyze_data && gunicorn --workers 2 weather.wsgi
