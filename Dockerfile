# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenClaw
RUN git clone https://github.com/openclaw/openclaw.git /tmp/openclaw && \
    cd /tmp/openclaw && \
    pip install -e . && \
    rm -rf /tmp/openclaw

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs

# Initialize database
RUN python scripts/init_db.py || true

# Expose port (if needed for web interface)
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["openclaw", "start", "--config", "openclaw_config.yaml"]
