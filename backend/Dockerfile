# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
# We don't have a requirements.txt yet, we've been using pip manually.
# Let's generate one or install packages manually in the dockerfile.
# Better to copy requirements if we had it.
# For now, let's install the known packages.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a requirements.txt first? No, I should create it now.
# Or I can just pip install the packages here. 
# Let's switch to copying the backend code first.

COPY . .

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
