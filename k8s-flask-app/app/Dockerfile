# Use Python 3.9 as base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy application files
COPY app.py requirements.txt ./

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt  # Ensure Flask & psycopg2 are installed

# Expose Flask app port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
