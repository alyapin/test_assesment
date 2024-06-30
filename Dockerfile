# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install libpq-dev to support psycopg2
RUN apt-get update && apt-get install -y libpq-dev \
    && apt-get install -y python3-dev

RUN apt-get install -y postgresql-client

# Copy and install Python dependencies
COPY requirements.txt .
COPY wait_for_pg.sh .
RUN pip install -r requirements.txt

# Copy the local scripts directory to the container
COPY src /src

# Define the command to run your Python script
CMD ["python3", "/src/fill_clients.py"]
