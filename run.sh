source install.sh
gunicorn -b 0.0.0.0:8080 api:app