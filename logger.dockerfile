FROM ubuntu:latest
RUN apt update && apt install python3 -y && apt clean
WORKDIR /app
COPY services/logger/logger.py .
CMD ["python3", "logger.py"]
