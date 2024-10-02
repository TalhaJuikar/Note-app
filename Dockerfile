# Use the official Ubuntu 22.04 image
FROM ubuntu:22.04

# Install Python, pip, and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file first for better caching
COPY requirements.txt .

# Create a virtual environment
RUN python3 -m venv venv

# Install dependencies in the virtual environment
RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["./venv/bin/python", "app.py"]

