FROM ubuntu

MAINTAINER J Goossens "<jgoos.code@gmail.com>"

WORKDIR ["/opt/convert"]

COPY sat5cfg2ansible.py requirements.txt .
COPY templates templates

RUN apt update \
    && apt install -y python3-pip python3 libmagic1 \
    && apt clean \
    && python3 -m pip install -r requirements.txt

VOLUME "/opt/convert/input_files"

