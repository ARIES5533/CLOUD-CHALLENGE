# Stage 1: Builder
FROM python:3.9-slim-buster as builder

# Set environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY auxiliary-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Image
FROM python:3.9-slim-buster


WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY auxiliary-service/app /app/app

# environment variable for the application
ENV AUX_SERVICE_VERSION=1.0.0

# Expose the internal port
EXPOSE 8001

# Command to run the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]