FROM ubuntu

MAINTAINER J Goossens "<jgoos.code@gmail.com>"

RUN apt update \
    && apt install -y python3-pip python3 libmagic1 \
    && apt clean \
    && python3 -m pip install python-magic

WORKDIR ["/opt/convert"]

VOLUME ["/opt/convert"]
