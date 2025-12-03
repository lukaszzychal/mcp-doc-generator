FROM python:3.12-slim

# Install system dependencies
# Combined into single RUN for better layer caching
RUN apt-get update && apt-get install -y \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-plain-generic \
    fonts-dejavu \
    graphviz \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install mermaid-cli
# Note: Railway has its own caching mechanisms, so we don't use cache mounts
RUN npm install -g @mermaid-js/mermaid-cli
# Note: draw.io export will use online API or Python library as fallback

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
# This layer will be cached if requirements.txt doesn't change
COPY requirements.txt .

# Install Python dependencies
# Note: Railway has its own caching mechanisms, so we don't use cache mounts
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
# This layer changes most frequently, so it's last
COPY src/ ./src/

# Create output directory
RUN mkdir -p /app/output

# Set Python path
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "src/server.py"]

