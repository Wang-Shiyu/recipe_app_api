FROM python:3.7-alpine
MAINTAINER Shiyu Wang

# Tell python not buffer the outputs and print them out directly
ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Create an empty folder on image
RUN mkdir /app
# Default location
WORKDIR /app
# From local machine to image
COPY ./app /app

# For security, avoiding docker iamge running app with root
# New user running the application only
RUN adduser -D sw
# Switch docker to the new user
USER sw
