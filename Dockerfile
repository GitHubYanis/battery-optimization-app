# Stage 1 — Build React
FROM node:18 AS frontend
WORKDIR /app/frontend
COPY frontend/package.json .
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2 — Backend Python + serve le frontend
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .

# Copie le build React dans un dossier static
COPY --from=frontend /app/frontend/dist ./static

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]