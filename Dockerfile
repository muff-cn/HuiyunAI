FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 安装系统依赖（如需额外依赖可在此添加）
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件并安装，利用 Docker 缓存加速构建
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# 复制项目到镜像中
COPY . /app

WORKDIR /app/backend

EXPOSE 8000

# 默认命令：运行 uvicorn（开发时可保留 --reload）
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
