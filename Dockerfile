FROM ubuntu:20.04
RUN apt-get update -y && ls -a
WORKDIR /..
ADD app.tar.gz ..
EXPOSE 80
RUN ./main
CMD ["./main"]
