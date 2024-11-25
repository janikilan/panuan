FROM ubuntu:20.04
RUN apt-get update -y
RUN ls -a
WORKDIR /..
ADD app.tar.gz ..
EXPOSE 80
RUN ls -a
CMD ["./main"]
