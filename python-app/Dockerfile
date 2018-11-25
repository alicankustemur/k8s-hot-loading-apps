FROM alpine:3.7

ADD . /code

WORKDIR /code

# All packages are versioned for idempotent.
RUN apk add --update python2==2.7.15-r2 py-pip==9.0.1-r1 py-mysqldb==1.2.5-r0

# All packages are versioned for idempotent.
RUN pip install Flask==1.0.2 MySQL-python==1.2.5 gunicorn==19.9.0