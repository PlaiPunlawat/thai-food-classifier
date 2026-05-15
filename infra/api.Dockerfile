FROM python:3.10-slim

WORKDIR /app

COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/api/ ./apps/api/
COPY packages/shared/ ./packages/shared/

ENV PYTHONPATH=/app:/app/packages/shared

WORKDIR /app/apps/api
EXPOSE 5000

CMD ["python", "index.py"]
