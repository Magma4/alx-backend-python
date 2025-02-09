# Use the official Python image as a base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django app into the container
COPY . .

# Expose the default Django port
EXPOSE 8000

# Command to start the Django app project
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
