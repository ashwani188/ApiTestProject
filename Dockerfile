# Use official Python image as base
FROM python:3.10-slim

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Clone the git repository (replace with your repo URL and branch)
RUN git clone -b ashwani_python https://github.com/ashwani188/ApiTestProject/ .

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Default command to run your main script (example: test_Class.py)
CMD ["python", "SeleniumDemo/test_Class.py"]
