FROM node:20 AS build
WORKDIR /build
COPY frontend/ .
RUN npm ci && npm run build

FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /build/dist /app/frontend/dist

COPY backend/ /app/backend/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
