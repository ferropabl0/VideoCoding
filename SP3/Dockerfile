FROM ubuntu:latest

RUN dpkg --configure -a && apt-get install -f

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y apt-utils && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg python3.10 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /Documents/GitHub/VideoCoding/SP3

RUN chmod +x /Documents/GitHub/VideoCoding/SP3/main.py

CMD ["./main.py"]

