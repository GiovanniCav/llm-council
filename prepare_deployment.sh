#!/bin/bash

# LLM Council - Web Package Generator
# This script prepares a clean folder for uploading to a web hosting service.

PACKAGE_DIR="LLM_Council_Web_Package"

echo "Creating Web Deployment Package..."

# 1. Clean and Create Directory
rm -rf "${PACKAGE_DIR}"
mkdir -p "${PACKAGE_DIR}"

# 2. Copy Necessary Files
cp -r backend "${PACKAGE_DIR}/"
mkdir -p "${PACKAGE_DIR}/frontend"
cp -r frontend/dist "${PACKAGE_DIR}/frontend/"
cp pyproject.toml "${PACKAGE_DIR}/"
cp uv.lock "${PACKAGE_DIR}/"
cp Dockerfile "${PACKAGE_DIR}/"
cp run_portable.sh "${PACKAGE_DIR}/"

# 3. Create README_DEPLOY.txt
cat > "${PACKAGE_DIR}/README_DEPLOY.txt" <<EOF
# LLM Council - Deployment Instructions

This folder contains everything needed to host the LLM Council app on the web.
Because this app runs a Python "brain" (Backend), you need a hosting provider that supports Python or Docker.

## Recommended Hosting Options

### Option 1: Render.com (Easiest)
1. Create a GitHub repository and upload the contents of this folder.
2. Sign up for Render.com.
3. Create a "Web Service".
4. Connect your repository.
5. Settings:
   - Runtime: Docker
   - Environment Variables: Add 'OPENROUTER_API_KEY' with your key.
6. Deploy!

### Option 2: Railway.app
1. Create a Railway project.
2. Drag and drop this folder (or connect GitHub).
3. It will auto-detect the Dockerfile.
4. Add your 'OPENROUTER_API_KEY' in the variables tab.

### Option 3: Standard Docker
You can build and run this container anywhere:
   docker build -t llm-council .
   docker run -p 8010:8010 -e OPENROUTER_API_KEY=your_key llm-council

## Important
NEVER upload your '.env' file or your API key directly to a public code repository.
Always use the hosting provider's "Environment Variables" settings to inject your key securely.
EOF

echo "✓ Created '${PACKAGE_DIR}'"
echo "This folder is ready to be uploaded to your hosting provider."
