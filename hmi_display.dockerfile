FROM python:3.12-slim
RUN pip install --no-cache-dir mysql-connector-python
WORKDIR /app
COPY hmi_display.py .
CMD ["python3", "-u", "hmi_display.py"]