# Stage 1: Build Vite React app
FROM node:18 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend ./
RUN npm run build

# Stage 2: Setup Django app
FROM python:3.11 AS backend
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy Django code
COPY . .

# Copy Vite build output into Nginx’s serving location
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# Collect Django static files
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
