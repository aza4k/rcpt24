#!/bin/bash
echo "Collecting static files..."
python3 manage.py collectstatic --noinput
echo "Migration running..."
python3 manage.py migrate --noinput
echo "Build finished successfully."
