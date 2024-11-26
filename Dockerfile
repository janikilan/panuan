FROM ubuntu:20.04

USER root
RUN apt-get update && apt-get install -y \
    python \
    git \
    curl \
    wget \
    socat

WORKDIR /root
COPY * root



