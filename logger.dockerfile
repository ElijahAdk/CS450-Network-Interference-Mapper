FROM ubuntu:latest
RUN apt update && apt install python3 -y && apt install mysql-connector-python -y && apt clean
WORKDIR /app
COPY logger.py .
CMD ["python3", "logger.py"]
