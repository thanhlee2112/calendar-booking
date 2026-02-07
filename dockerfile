FROM python:3.12-slim

# Ngăn chặn các câu hỏi tương tác khi build
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết cho mysqlclient
# Chúng ta thêm: pkg-config và default-libmysqlclient-dev, gcc
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Nâng cấp pip và cài đặt dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]