# 阶段 1：构建依赖
FROM python:3.10-slim AS builder

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt
COPY requirements.txt .

# 安装构建依赖和项目依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 阶段 2：运行镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制构建阶段的依赖
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 复制项目文件
COPY . .

# 安装 Gunicorn
RUN pip install gunicorn

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# 暴露端口
EXPOSE 8000

# 运行 Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project.wsgi:application"]