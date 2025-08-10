# Use Python 3.10 base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose Django's default port
EXPOSE 8000

# Run Django server (note: -p is part of docker run, but here we keep "0.0.0.0:8000" to bind correctly)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
