# pull official base image
FROM python:3.9

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
# install dependencies
RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get install -y netcat-traditional

# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev \
#     && apk add --no-cache --virtual build-deps jpeg-dev zlib-dev libjpeg linux-headers libffi-dev \        
#     && pip install Pillow uwsgi

COPY ./requirements.txt .
RUN pip install -r requirements.txt


# copy entrypoint.sh
COPY ./entrypoint.sh .


# copy project
COPY . .

RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]
# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
