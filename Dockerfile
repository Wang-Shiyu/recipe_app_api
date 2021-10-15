FROM python:3.7-alpine
MAINTAINER Shiyu Wang

# Tell python not buffer the outputs and print them out directly
ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

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
