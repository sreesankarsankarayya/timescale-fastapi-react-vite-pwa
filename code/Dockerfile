# Stage 1: Build the React Vite frontend
FROM node:16-alpine as frontend-build
WORKDIR /app/frontend
# Copy package files and install dependencies
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
# Copy all frontend source code and build the app
COPY frontend .
RUN npm run build

# Stage 2: Build the Python backend
FROM python:3.10-slim
WORKDIR /app
# Copy backend dependencies and install them
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the backend code
COPY backend .
# Copy the built frontend static files into the "static" directory
COPY --from=frontend-build /app/frontend/dist ./static

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
