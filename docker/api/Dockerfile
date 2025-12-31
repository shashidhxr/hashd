FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app ./app

ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["flask", "--app", "app.api.server", "run", "--host=0.0.0.0", "--port=5000"]
