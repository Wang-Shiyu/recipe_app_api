FROM python:3.7-alpine
MAINTAINER Shiyu Wang

# Tell python not buffer the outputs and print them out directly
ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt /requirements.txt
# Remain in container
RUN apk add --update --no-cache postgresql-client jpeg-dev
# Remove from container
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
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
# Store static and media file without permission errors
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D sw
RUN chown -R sw:sw /vol/
# Owner can do everything with the directory and the rest can read and execute
# from the directory.
RUN chmod -R 755 /vol/web
# Switch docker to the new user
USER sw
