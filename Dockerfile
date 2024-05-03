# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Install necessary libraries
RUN apt-get update && apt-get install -y libgl1-mesa-dev libglib2.0-0

# Copy only the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Run TeslaThermalCam.py when the container launches
CMD ["python", "TeslaThermalCam.py"]
