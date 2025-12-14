# ===== مرحله 1: Build frontend =====
FROM node:20-alpine as frontend-build
WORKDIR /app/frontend

# نصب npm dependencies
COPY frontend/package*.json ./
RUN npm install

# کپی کل frontend و build
COPY frontend/ ./
RUN npm run build   # فرض بر اینه خروجی build داخل /dist باشد

# ===== مرحله 2: Setup Python backend و Workers =====
FROM python:3.11-slim
WORKDIR /app

# نصب dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get update && apt-get install -y curl nginx bash

# کپی backend و workerها
COPY coordinator/ ./coordinator/
COPY worker/ ./worker/

# کپی frontend build به nginx
COPY --from=frontend-build /app/frontend/dist /usr/share/nginx/html

# nginx config
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# expose ports (Railway با PORT env کار می‌کند)
EXPOSE 80 8000 8001 8002 8003 8004

# ===== Run coordinator, workers و nginx =====
CMD bash -c "\
  echo 'Starting coordinator...' && \
  uvicorn coordinator.api:app --host 0.0.0.0 --port 8000 & \
  echo 'Starting worker1...' && \
  uvicorn worker.app:app --host 0.0.0.0 --port 8001 & \
  echo 'Starting worker2...' && \
  uvicorn worker.app:app --host 0.0.0.0 --port 8002 & \
  echo 'Starting worker3...' && \
  uvicorn worker.app:app --host 0.0.0.0 --port 8003 & \
  echo 'Starting worker4...' && \
  uvicorn worker.app:app --host 0.0.0.0 --port 8004 & \
  echo 'Starting nginx...' && \
  nginx -g 'daemon off;' \
"
