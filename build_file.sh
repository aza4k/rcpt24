#!/bin/bash
echo "🚀 Build started..."
pip install -r requirements.txt
python3 manage.py collectstatic --noinput
python3 manage.py migrate
echo "✅ Build completed!"
