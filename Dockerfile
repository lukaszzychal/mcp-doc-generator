FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-plain-generic \
    fonts-dejavu \
    graphviz \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for mermaid-cli (using Debian package)
RUN apt-get update && apt-get install -y nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# Install mermaid-cli and draw.io dependencies globally
RUN npm install -g @mermaid-js/mermaid-cli
# Note: draw.io export will use online API or Python library as fallback

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Create output directory
RUN mkdir -p /app/output

# Set Python path
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "src/server.py"]

