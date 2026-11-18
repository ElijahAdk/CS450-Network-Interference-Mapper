FROM ubuntu:latest
RUN apt update && apt install python3 -y && apt install sense-hat -y && apt clean
WORKDIR /app
COPY poller.py .
CMD ["python3", "poller.py"]
