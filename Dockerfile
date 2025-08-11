FROM python:3.11.2-slim-buster

WORKDIR /app
COPY . /app

# Install AWS CLI and dependencies in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    awscli \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]
