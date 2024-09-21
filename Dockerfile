# Use the official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    default-libmysqlclient-dev \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy package.json and tailwind.config.js
COPY package.json /app/
COPY tailwind.config.js /app/

# Install npm dependencies for Tailwind CSS
RUN npm install

# Create necessary static directories (css/dist)
RUN mkdir -p ./static/css/dist && \
    echo '@tailwind base;\n@tailwind components;\n@tailwind utilities;' > ./static/css/dist/input.css

# Build Tailwind CSS before collecting static files
RUN npx tailwindcss -i ./static/css/dist/input.css -o ./static/css/dist/styles.css --minify

# Copy the rest of the project files
COPY . /app/

# Collect static files (run collectstatic in Django)
RUN python manage.py collectstatic --noinput

# Expose Django port
EXPOSE 8000

# Run Django app
CMD ["gunicorn", "frankfurt_school_manager.wsgi:application", "--bind", "0.0.0.0:8000"]
