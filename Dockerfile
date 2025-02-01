# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /db_load

# Copy the current directory contents into the container at /app
COPY db_load /db_load

# Install necessary Python packages explicitly
RUN pip install --no-cache-dir python-dotenv neo4j

# Run indexing.py when the container launches
CMD ["python", "indexing.py"]