FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN mkdir -p /var/log/auth-service

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV SERVICE_NAME=auth-service
EXPOSE 8000
CMD ["/entrypoint.sh"]
