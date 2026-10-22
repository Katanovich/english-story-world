FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN useradd --create-home appuser && mkdir -p /data/media && chown appuser /data/media
USER appuser

EXPOSE 8000
CMD ["sh", "/app/docker-entrypoint.sh"]
