# Use a base Python image
FROM python:3.10

# create and set the working directory
RUN mkdir -p /app

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies from the requirements.txt
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port your Django app runs on (default 8000)
EXPOSE 8000

# Set the entry point for the container to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
