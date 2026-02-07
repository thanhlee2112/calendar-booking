from .base import *

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
allowed_hosts_env = os.getenv("DJANGO_ALLOWED_HOSTS")
if allowed_hosts_env:
    # Tách chuỗi bằng dấu phẩy thành một danh sách
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(",")]
else:
    # Nếu trống hoàn toàn, mặc định cho phép localhost để tránh sập app
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]