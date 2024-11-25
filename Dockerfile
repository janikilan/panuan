FROM ubuntu:20.04
RUN apt-get update && apt-get install -y python3
WORKDIR /home/app
ADD app.tar.gz /app
EXPOSE 80
RUN lscpu && ls -a
CMD ["ls"]
