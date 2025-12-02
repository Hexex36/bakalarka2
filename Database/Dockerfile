# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY option_fetch.py .
COPY config.toml .

# Command to run the application
CMD ["sh", "-c", "sed -i 's/host = \"localhost\"/host = \"timescaledb\"/' config.toml && python option_fetch.py"]
