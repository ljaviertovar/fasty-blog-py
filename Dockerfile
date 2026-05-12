FROM node:20 AS nodebuild
WORKDIR /app

# Install Node deps and build TailwindCSS assets.
ENV NODE_ENV=development
# Copy only package files first to leverage Docker cache
COPY tailwindcss/package*.json ./tailwindcss/
RUN cd tailwindcss && npm ci --no-audit --no-fund

# Copy Tailwind config and source
COPY tailwind.config.js .
COPY tailwindcss/ ./tailwindcss/

# Copy templates so Tailwind can scan them
COPY templates/ ./templates/

# Create output directory for CSS and build Tailwind
RUN mkdir -p /app/static/css && cd /app/tailwindcss && npm run build:css

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

# Install Python dependencies from requirements.txt
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Use PORT env var from the platform (Render sets $PORT)
CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-8000} --workers 3"]
