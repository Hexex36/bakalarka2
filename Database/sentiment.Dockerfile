# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY sentiment_requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r sentiment_requirements.txt

RUN playwright install

# Copy the rest of the application code
COPY sentiment_fetch.py .
COPY redirect_resolver.py .
COPY config.toml .
COPY headers.json .

# Command to run the script
CMD ["python", "sentiment_fetch.py"]
