# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the libraries needed for cv2
RUN apt-get update && apt-get install -y libgl1-mesa-dev libglib2.0-0

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . /app

# Establece las variables de entorno necesarias para Flask
ENV FLASK_APP run.py
ENV FLASK_ENV development

# Expone el puerto 5000 para Flask
EXPOSE 5000

# Comando por defecto para ejecutar la aplicación Flask
CMD flask run --host=0.0.0.0 --port=5000