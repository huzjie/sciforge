# 构建阶段可选：直接以 Python 运行（核心零依赖，serve 需要 fastapi/uvicorn）
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi "uvicorn[standard]" 2>/dev/null || true

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["python", "-m", "sciforge", "serve", "--host", "0.0.0.0", "--port", "8000"]
