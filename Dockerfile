FROM python:3.11-slim
# Using slim version reduces image size by ~700MB compared to full python image

WORKDIR /app
# Sets working directory to /app inside container

# Install system dependencies needed for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*
# gcc/g++ needed for packages like scikit-learn, xgboost
# curl needed for health check
# --no-install-recommends avoids extra packages, reduces size
# rm -rf cleans up apt cache to reduce image size

# Copy requirements first for better caching
COPY requirements.txt .
# Copying requirements separately allows Docker to cache this layer
# If requirements don't change, this layer stays cached

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# --no-cache-dir prevents pip from storing downloaded packages locally

COPY . .
# Copies all project files to /app in container

# Create non-root user for security
RUN useradd -r -s /bin/bash appuser && \
    chown -R appuser:appuser /app
# Running as non-root prevents potential security vulnerabilities
USER appuser
# Switch to non-root user

# Health check to monitor container health
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1
# Checks every 30s if app responds on port 5000
# --start-period=5s gives app 5s to start before first check

EXPOSE 5000
# Documents that container listens on port 5000
# Note: EXPOSE doesn't actually publish the port

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
# PYTHONUNBUFFERED=1 ensures Python output appears in logs immediately

CMD ["python3", "app.py"]
# Default command when container starts
