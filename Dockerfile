# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./google_sheets_script.py .
COPY ./config_script.py .
RUN pip install -r requirements.txt

ADD google_sheets_script.py /
CMD [ "python", "./google_sheets_script.py" ]

# copy project
COPY . .