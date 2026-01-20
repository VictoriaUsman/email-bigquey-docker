FROM python:3.11-slim

# Set environment variables immediately
ENV DAGSTER_HOME=/opt/dagster/app
ENV PYTHONPATH="/opt/dagster/app:${PYTHONPATH}"
ENV PATH="/usr/local/bin:$PATH"

WORKDIR /opt/dagster/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files
COPY . .

# Explicitly grant execution permissions just in case
RUN chmod +x /usr/local/bin/dagster*