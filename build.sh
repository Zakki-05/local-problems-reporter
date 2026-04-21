#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Download and run Tailwind CSS standalone CLI for Linux (Render environment)
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
chmod +x tailwindcss-linux-x64
./tailwindcss-linux-x64 -i ./static/css/input.css -o ./static/css/tailwind.css --minify

python manage.py collectstatic --no-input
python manage.py migrate
