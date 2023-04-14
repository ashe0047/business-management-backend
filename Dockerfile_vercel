# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim


# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image.
COPY . .

# Run migration for Django
RUN python manage.py migrate --noinput

# Collect the static files in static folder
RUN python manage.py collecstatic --noinput


# Run the web service on container startup. Here we use the gunicorn
CMD exec gunicorn --bind 0.0.0.0:$PORT businessmanagement.wsgi:application