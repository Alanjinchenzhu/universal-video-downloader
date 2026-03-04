# VideoDL 后端 Dockerfile
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 使用国内镜像源
RUN echo 'deb http://mirrors.aliyun.com/debian/ trixie main non-free non-free-firmware' > /etc/apt/sources.list && \
    echo 'deb http://mirrors.aliyun.com/debian/ trixie-updates main non-free non-free-firmware' >> /etc/apt/sources.list && \
    echo 'deb http://mirrors.aliyun.com/debian/ trixie-backports main non-free non-free-firmware' >> /etc/apt/sources.list

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY main.py .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
