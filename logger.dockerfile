FROM ubuntu:latest
RUN apt update && apt install python3 -y && apt clean
WORKDIR /app
COPY logger.py .
CMD ["python3", "logger.py"]
