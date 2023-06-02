# Use an official Python runtime as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the project files to the working directory
COPY poetry.lock pyproject.toml /code/

# Install dependencies
RUN pip install --no-cache-dir poetry && \
  poetry config virtualenvs.create false && \
  poetry install --no-dev

# Copy the remaining project files
COPY . /code/


# Expose the Django development server port
EXPOSE 8000

# Start the Django development server
CMD python manage.py runserver 0.0.0.0:8000


