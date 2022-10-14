# pull official base image
FROM python:3.10.7-slim-buster

# set work directory
WORKDIR /tasmopot

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /tasmopot
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy project
COPY . /tasmopot

CMD ["gunicorn", "--bind", " 0.0.0.0:5000", "wsgi:app"]