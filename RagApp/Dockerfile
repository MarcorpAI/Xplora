FROM python:3.11.1

# Set working directory inside the container
WORKDIR /usr/src/app

# Install build dependencies (using apk package manager)
RUN apt-get update && \
    apt-get install -y gcc  libffi-dev libssl-dev

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip


# Copy requirements.txt and install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt


RUN pip install --quiet --no-cache-dir -r requirements.txt



# Copy entrypoint script
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# Copy application code
COPY . /usr/src/app/

# Set entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
