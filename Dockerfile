# Lightweight Python container for Artifact Evaluation
FROM python:3.10-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy artifact code, models, and data
COPY . .

# Create output directory for figures
RUN mkdir -p output_figures

# Default execution: run the complete verification suite
ENTRYPOINT ["python", "reproduce_all.py"]
