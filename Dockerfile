# Use the official Python image from DockerHub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application files to the working directory
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 5000

# Use Gunicorn to serve the app using the factory function
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "userbase:create_app()"]
