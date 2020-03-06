FROM alpine:3.7

ADD . /code

WORKDIR /code

RUN apk add --update --no-cache \
        python2 \
        py-pip \
        py-mysqldb \
    && pip install \
        Flask \
        MySQL-python \
        gunicorn \
    && rm -rf /var/cache/apk/*