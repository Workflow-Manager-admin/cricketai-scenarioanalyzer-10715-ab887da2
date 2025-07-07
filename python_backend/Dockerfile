# Use official Python image as the base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Ensure start.sh has execute permission
RUN chmod +x start.sh

# Expose API port
EXPOSE 3001

# Start the FastAPI server via the start script
CMD ["./start.sh"]
