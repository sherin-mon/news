# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory content into the container
COPY . .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ensure that environment variables from the `.env` file are loaded
RUN pip install python-dotenv

# Expose port 8000 (since your app runs on port 8000)
EXPOSE 8000

# Set the environment to production mode (optional)
ENV FLASK_ENV=production

# Run the Flask application
CMD ["python", "app.py"]

