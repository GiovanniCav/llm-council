# LLM Council: Technical Handover Specification & Project Report

This document provides a comprehensive overview of the modifications, architectural decisions, and technical specifications for the **LLM Council** project. It is intended for AI agents or developers to quickly understand the current state, implementation details, and critical learnings of the project.

---

## 🛰️ Project Overview
The **LLM Council** is a multi-model orchestration platform. It allows users to query a group of distinct LLMs (the "Council"), which then critique and rank each other's responses, before a terminal "Chairman" model synthesizes a final, high-quality answer.

---

## 🏗️ Core Architecture

### **Frontend (Vite + React)**
- **Static Assets**: Compiled into optimized JS/CSS via `npm run build`.
- **API Communication**: Uses relative paths (`/api/...`) via `frontend/src/api.js`, allowing the frontend to be served from the same origin as the backend.
- **Port Branding**: Hardcoded as `(8010)` in `index.html` and `Sidebar.jsx` to distinguish this specific instance.

### **Backend (FastAPI + Python)**
- **Unified Server**: The backend is configured to serve both the API and the static frontend assets from `frontend/dist`.
- **Primary Endpoint**: Port **8010** (configurable via `.env`).
- **Storage**:
    - **Conversations**: Stored as individual JSON files in `data/conversations/`.
    - **Activity Logs**: Appends transaction data to `logs/activity.jsonl`.

---

## 🚀 Key Features & Implementations

### **1. Unified Portability (`run_portable.sh`)**
A specialized shell script that simplifies local execution into a single command.
- **Cleanup Logic**: Automatically finds and terminates any process on port `8010` using `lsof` and `kill -9` before starting.
- **Unified Process**: Runs the FastAPI server, which mounts the `frontend/dist` directory for simultaneous serving.

### **2. MacOS Desktop App (`LLM Council.app`)**
A native MacOS application bundle generated via `create_mac_app.sh`.
- **Bundle Logic**: Contains a `Launcher` script in `Contents/MacOS/` that uses `osascript` to open a Terminal window and execute the portable script.
- **App Icon**: Uses a custom-generated high-resolution `.icns` file located in `Contents/Resources/AppIcon.icns`.

### **3. Comprehensive Activity Logging**
A robust transaction logger located in `backend/logger.py`.
- **Format**: JSONL (JSON Lines) for efficient appending.
- **Data Depth**: Logs the user prompt, final synthesis, **full Stage 1 model responses**, **full Stage 2 peer critiques/rankings**, and aggregate ranking metadata.

### **4. Web Deployment Package**
A "ready-to-ship" folder created by `prepare_deployment.sh`.
- **Docker Integration**: Includes a `Dockerfile` using `uv` for high-performance dependency management.
- **Instructions**: Comes with `README_DEPLOY.txt` detailing setup for **Render**, **Railway**, and Docker.

---

## 🧠 Critical Learnings & Pitfalls

### **Icon Generation & MacOS Cache**
- **Pitfall**: MacOS `iconutil` is very sensitive to pixel formats. We initially had an image that was technically a JPEG but used a PNG extension; this caused silent failures in the `.icns` creation.
- **Solution**: Always force a `sips` conversion to PNG before running `iconutil`.
- **Pitfall**: The MacOS Finder often caches app icons. Even after the file is fixed, the icon might not appear.
- **Solution**: Use the `touch` command on the `.app` bundle or use `Cmd+I` (Get Info) in Finder to force a refresh.

### **Process Management & Port Collisions**
- **Pitfall**: When restarting the app quickly, Python's `uvicorn` might hang on the port or the previous background process might still be active.
- **Solution**: Implement `lsof -ti:PORT | xargs kill -9` in all startup scripts to ensure a clean bind.

### **Path Resolution**
- **Pitfall**: Using `__file__` based paths can behave differently when run via `uv run` vs a traditional python interpreter depending on the CWD.
- **Solution**: Use `os.getcwd()` for directory creation in scripts intended to run from the project root to ensure folders like `logs/` end up in the expected location.

---

## 🔧 Technical Specs for the Next Bot

- **Working Directory**: All commands must be run from the project root.
- **Environment**: Requires `.env` with `OPENROUTER_API_KEY`.
- **Default Port**: `8010`.
- **Primary Entrypoints**:
    - Local: `./run_portable.sh`
    - Full Setup: `./start.sh` (Backend + Frontend Dev Server)
    - Deployment Prep: `./prepare_deployment.sh`

## 📊 Status Summary
The project is currently stable, fully portable, and uniquely branded to port 8010. The logging system is highly granular, capturing the full deliberation process of the council.
