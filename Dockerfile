# Use the official Python image based on Ubuntu 22.04
FROM python:3.10-slim-bullseye

# Install build-essential for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file first for better caching
COPY requirements.txt .

# Install dependencies directly without creating a virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Accept build arguments for database credentials
ARG DB_HOST
ARG DB_NAME
ARG DB_USER
ARG DB_PASS

# Create the .env file with the database credentials
RUN echo "DB_HOST=${DB_HOST}" > .env && \
    echo "DB_NAME=${DB_NAME}" >> .env && \
    echo "DB_USER=${DB_USER}" >> .env && \
    echo "DB_PASS=${DB_PASS}" >> .env

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["flask", "run"]