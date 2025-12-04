# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY sentiment_requirements.txt .

# Install python packages and system dependencies
RUN apt-get update && \
    pip install --no-cache-dir -r sentiment_requirements.txt && \
    playwright install-deps && \
    playwright install && \
    rm -rf /var/lib/apt/lists/*


# Copy the rest of the application code
COPY sentiment_fetch.py .
COPY redirect_resolver.py .
COPY config.toml .
COPY headers.json .

# Command to run the script
CMD ["python", "sentiment_fetch.py"]
