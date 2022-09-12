FROM ubuntu

LABEL org.opencontainers.image.authors="jgoos.code@gmail.com"

WORKDIR /prog

ENV PATH="/prog:$PATH"

COPY sat5cfg2ansible.py requirements.txt .
COPY templates templates

RUN apt update \
    && apt install -y python3-pip python3 libmagic1 \
    && apt clean \
    && python3 -m pip install -r requirements.txt

VOLUME /data

CMD ["python3", "./sat5cfg2ansible.py", "/data"]
