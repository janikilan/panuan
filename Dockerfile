FROM ubuntu:20.04
RUN apt-get update -y && ls -a
WORKDIR /home/app
ADD app.tar.gz /app
EXPOSE 80
RUN lscpu && ls -a
CMD ["./main"]
