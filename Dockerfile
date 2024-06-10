# Use an official Python runtime as a parent image
FROM python:3.12 AS python-build
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.12-slim
COPY --from=python-build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends gcc git curl libpq-dev mariadb-client libmariadb-dev wget libmariadb3 libmariadb-dev \
    && rm -rf /var/cache/apt/archives /var/lib/apt/lists/* \
    && apt-get clean

# Copy project
COPY . .

# Install Python dependencies
RUN pip3 install --upgrade pip

# Expose port 8000
EXPOSE 8001

# Command to run the Django application
CMD ["bash", "mariadb.sh"]
