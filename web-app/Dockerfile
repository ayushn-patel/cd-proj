# Use Python runtime as the base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 5000 for Flask
EXPOSE 5000

# Environment variable to run Flask in production
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]