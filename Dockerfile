FROM ubuntu:20.04

USER root
#EXPOSE 80
RUN apt-get update && apt-get install -y \
    python \
    git \
    curl \
    socat

WORKDIR /root
COPY . .
RUN pip install -r requirements.txt
RUN chmod u+x *
RUN python run.py -u https://google.com -p list.txt
