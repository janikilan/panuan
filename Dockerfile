FROM ubuntu:20.04

USER root
RUN apt-get update && apt-get install -y \
    python \
    git \
    curl \
    socat

WORKDIR /root
COPY . .
RUN ls -a


