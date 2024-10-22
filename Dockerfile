# Use the official Python image from Docker Hub
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port that the Flask app runs on
EXPOSE 5000

# Set environment variables to run the app
ENV FLASK_APP=flask_app/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app
CMD ["flask", "run"]
