# Use official Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for psycopg2 (PostgreSQL adapter)
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Default command (production-grade WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]