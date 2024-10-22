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

# Set environment variables for Flask
ENV FLASK_APP=userbase:create_app()
ENV FLASK_ENV=production

# Run database migrations and start the Flask server
CMD ["sh", "-c", "flask db upgrade && flask run --host=0.0.0.0 --port=5000"]
