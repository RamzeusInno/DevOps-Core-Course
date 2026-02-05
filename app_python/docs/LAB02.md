# Lab 2 — Docker Containerization: Implementation Report

## Docker Best Practices Applied

### 1. Non-Root User Implementation
**What:** Created a dedicated user and switched to it using the `USER` directive.
**Why:** Reduces security risks.

### 2. Specific Base Image Version
**What:** Used `python:3.12-slim` instead of `python:3.12` or `python:latest`.
**Why:** The slim version is smaller and contains only essential packages.

### 3. Layer Caching Optimization
**What:** Copied `requirements.txt` first, installed dependencies, then copied application code.
**Why:** When code changes but dependencies don't, Docker can reuse cached layers from the dependency installation, which increases up rebuilds speed.

### 4. .dockerignore File
**What:** Created a `.dockerignore` file to exclude unnecessary files from the build context.
**Why:** Reduces build context size and prevents unnecessary files from being included in the image.

### 5. WORKDIR Directive
**What:** Set `/app` as the working directory using `WORKDIR`.
**Why:** Ensures all subsequent commands run in a consistent directory and makes the Dockerfile more readable.

### 6. No Cache for pip
**What:** Used `pip install --no-cache-dir` to avoid storing pip cache in the image.
**Why:** Reduces image size by not including unnecessary cache files.

## Image Information & Decisions

### Base Image Selection
- **Chosen:** `python:3.12-slim`
- **Reasoning:** 
  - **Slim vs Alpine:** Chose slim for better compatibility with Python packages
  - **Version pinning:** Used specific version (3.12) rather than `latest` for reproducibility
  - **Size comparison:** `slim` (~123MB) vs `full` (~320MB)

### Final Image Size
- **Base image:** 123MB (python:3.12-slim)
- **Final image:** 145MB
- **Increase:** 22MB (application + Flask dependencies)

### Layer Structure Analysis
```bash
# Check layers with docker history
docker history ramzeus1/devops-info-service:lab2