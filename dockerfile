# Sử dụng Python bản nhẹ (slim) để tiết kiệm dung lượng VPS
FROM python:3.12-slim

# Thiết lập biến môi trường để Python không tạo file .pyc và log được xuất thẳng ra console
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết cho Postgres
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Cài đặt thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Chạy server bằng Gunicorn (thay vì manage.py runserver để chịu tải tốt hơn)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]