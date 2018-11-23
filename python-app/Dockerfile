FROM alpine:3.7

ADD . /code

WORKDIR /code

RUN apk add --update python2 py-pip

RUN pip install Flask==1.0.0