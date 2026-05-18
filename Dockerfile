# Dockerfile for LLM Council

# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (none strictly needed for slim, but good practice)
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*

# Install uv for fast package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY backend ./backend
COPY frontend/dist ./frontend/dist
COPY run_portable.sh ./run_portable.sh

# Install Python dependencies
RUN uv sync --frozen

# Expose port
EXPOSE 8001

# Run the app
CMD ["uv", "run", "python", "-m", "backend.main"]
