# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory in the container
COPY main.py /app/


# Expose port 8000
EXPOSE 8000

# Command to run the app
CMD ["python", "main.py"]