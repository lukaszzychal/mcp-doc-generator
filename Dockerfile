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

# Install mermaid-cli with cache mount for faster rebuilds
RUN --mount=type=cache,target=/root/.npm \
    npm install -g @mermaid-js/mermaid-cli
# Note: draw.io export will use online API or Python library as fallback

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
# This layer will be cached if requirements.txt doesn't change
COPY requirements.txt .

# Install Python dependencies with cache mount
# Cache mount speeds up pip install on subsequent builds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

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

