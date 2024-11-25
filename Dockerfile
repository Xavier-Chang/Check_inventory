# Use the official Python slim image as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents to the container
COPY . .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the Python script
CMD ["python", "loewe_stock_checker.py"]
