# Use Python official image as a parent
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/ .

# Expose the Flask app port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
