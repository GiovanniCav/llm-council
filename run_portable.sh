#!/bin/bash

# LLM Council - Portable Start Script
# This script runs the bundled application (Backend + Frontend) from a single process.

echo "Starting Portable LLM Council..."
# Kill anything on port 8010
lsof -ti:8010 | xargs kill -9 2>/dev/null
echo "Backend and Frontend will be served from http://localhost:8010"
echo ""

# Ensure .env exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Please create one with your OPENROUTER_API_KEY."
    exit 1
fi

# Run the backend (which now also serves the frontend)
# Try uv first, fall back to python if uv is not available
if command -v uv &> /dev/null; then
    uv run python -m backend.main
else
    echo "Note: 'uv' not found, using python directly."
    python -m backend.main
fi
