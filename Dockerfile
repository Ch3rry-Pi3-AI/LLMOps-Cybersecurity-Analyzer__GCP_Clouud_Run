# ------------------------------
# Build Stage: Frontend (Next.js)
# ------------------------------
FROM node:20-alpine AS frontend-build

# Set working directory for the frontend build
WORKDIR /app

# Copy package metadata and install dependencies
COPY frontend/package*.json ./
RUN npm ci

# Copy the full frontend source code
COPY frontend/ .

# Generate the static Next.js build output (placed in /app/out)
RUN npm run build


# ------------------------------
# Production Stage: Backend (FastAPI)
# ------------------------------
FROM python:3.12-slim

# Set working directory in final image
WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager)
RUN pip install uv

# Copy backend dependency files and install them
COPY backend/pyproject.toml backend/uv.lock* ./
RUN uv sync --frozen

# Copy backend application source
COPY backend/ ./

# Copy Next.js static export into the backend "static" directory
COPY --from=frontend-build /app/out ./static


# ------------------------------
# Health Check
# ------------------------------
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1


# ------------------------------
# Networking Configuration
# ------------------------------
EXPOSE 8000


# ------------------------------
# Application Startup
# ------------------------------
CMD ["uv", "run", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
