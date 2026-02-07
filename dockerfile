FROM python:3.12-slim
RUN apt-get update && apt-get install -y libmysqlclient-dev pkg-config gcc && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn whitenoise
COPY . .
# Script để khởi chạy
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]