# DevOps Info Service (Python)

![Python CI](https://github.com/RamzeusInno/DevOps-Core-Course/actions/workflows/python-ci.yml/badge.svg)

## Overview
The DevOps Info Service is a production-ready web application that reports detailed information about its runtime environment, system resources, and service status. This service will evolve throughout the DevOps course into a comprehensive monitoring tool.

## Prerequisites
- Python 3.11+
- pip

## Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Application
```bash
python app.py
# Custom configuration
PORT=8080 python app.py
HOST=127.0.0.1 PORT=3000 DEBUG=true python app.py
# http://127.0.0.1:3000
```

## API Endpoints
- `GET /` — Service, system, runtime, request info, and endpoint list.
- `GET /health` — Health status and uptime (HTTP 200).

## Configuration
Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST`   | `0.0.0.0` | Bind address |
| `PORT`   | `8080`  | Listening port |
| `DEBUG`  | `False` | Enable Flask debug mode |

## Notes
- Logging is configured at startup; noisy werkzeug logs are suppressed to WARNING.
- Error handlers return JSON for 404 and 500.

## Docker

### Build the Image
```bash
docker build -t yourusername/devops-info-service:latest .
```
### Run container
``` bash
docker run -d -p 5000:5000 --name devops-app ramzeus1/devops-info-service:latest

# Check logs
docker logs devops-app

# Stop container
docker stop devops-app
docker rm devops-app
```