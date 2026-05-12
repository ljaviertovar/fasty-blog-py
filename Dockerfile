FROM node:18 AS nodebuild
WORKDIR /app

# Build TailwindCSS assets
COPY tailwindcss/ ./tailwindcss/
RUN cd tailwindcss && npm ci && (npm run build || npx tailwindcss -i input.css -o ../static/css/main.css --minify)

FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system build deps (if needed) and clean up
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc && rm -rf /var/lib/apt/lists/*

# Copy Python project files
COPY . .

# Copy built static assets from node stage
COPY --from=nodebuild /app/static ./static

# Install Python dependencies. Prefer requirements.txt, fallback to installing package
RUN bash -lc "python -m pip install --upgrade pip && (if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; else pip install --no-cache-dir .; fi)"

EXPOSE 8000

# Use PORT env var from the platform (Render sets $PORT)
CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-8000} --workers 3"]
