FROM python:3.11-slim

# Install ffmpeg and jq
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg jq && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ .
COPY run.sh /

# Make run script executable
RUN chmod +x /run.sh

# Expose port
EXPOSE 8099

# Run
CMD ["/run.sh"]
