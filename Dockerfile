FROM python:3.10-slim

WORKDIR /app

# 先安装依赖（利用Docker缓存层）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再复制代码
COPY . .

# 设置生产环境变量
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# 使用非root用户运行（安全最佳实践）
RUN useradd -m myuser && chown -R myuser:myuser /app
USER myuser

# 使用waitress作为生产级WSGI服务器
CMD ["python", "app.py"]