# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application directory into the container
COPY ./app /code/app

# Add the project root to the PYTHONPATH
# This tells Python where to look for the 'app' module
ENV PYTHONPATH "${PYTHONPATH}:/code"

# Expose port 80 for the application to listen on
EXPOSE 80

# Command to run the application, pointing to the app object in app/main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
