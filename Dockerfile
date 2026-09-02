# Use a lightweight official Python image
FROM python:3.11-slim

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Display Python output immediately in Docker logs
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy dependency list first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy FastAPI source files
COPY main.py .
COPY schemas.py .

# Copy the trained model
COPY model/ ./model/

# Document the application's default port
EXPOSE 8000

# Start FastAPI using Uvicorn
# PORT defaults to 8000 but can be supplied by a cloud host
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
