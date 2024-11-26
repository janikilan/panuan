FROM ubuntu:20.04

USER root
#EXPOSE 80
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    curl \
    socat

WORKDIR /root
COPY . .
RUN pip install -r requirements.txt
RUN chmod u+x *
RUN python3 run.py -u https://google.com:80 -x list.txt -p socks5
