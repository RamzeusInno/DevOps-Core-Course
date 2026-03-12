```markdown
# Lab 7: Observability & Logging with Loki Stack

**Name:** Ramzeus
**Date:** 2026-03-12
**Lab Points:** 10

---

## Architecture

The system consists of 4 components:

- **Loki 3.0**: Log storage with TSDB index
- **Promtail 3.0**: Log collector from Docker containers
- **Grafana 12.3**: Visualization and LogQL queries
- **app-python**: Test Flask application with JSON logging

All components communicate through a dedicated Docker network. Promtail reads container logs via Docker socket and forwards them to Loki. Grafana queries Loki and provides visualization.

---

## Task 1: Deploy Loki Stack (4 pts)

### Loki Configuration

**File:** `monitoring/loki/config.yml`

```yaml
auth_enabled: false

server:
  http_listen_port: 3100

common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2020-10-24
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h

storage_config:
  tsdb_shipper:
    active_index_directory: /loki/tsdb-index
    cache_location: /loki/tsdb-cache
  filesystem:
    directory: /loki/chunks

limits_config:
  retention_period: 168h

compactor:
  working_directory: /loki/compactor
  retention_enabled: true
```

### Promtail Configuration

**File:** `monitoring/promtail/config.yml`

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'
      - source_labels: ['__meta_docker_container_label_logging']
        regex: 'promtail'
        target_label: 'logging'
        action: keep
      - source_labels: ['__meta_docker_container_label_app']
        regex: '(.+)'
        target_label: 'app'
```

### Docker Compose Configuration

**File:** `monitoring/docker-compose.yml`

The compose file defines four services: loki, promtail, grafana, and app-python. Each service has:
- Resource limits (CPU and memory)
- Health checks
- Dependencies
- Persistent volumes for data

### Deployment

```bash
cd ~/devops_lab5/monitoring
docker compose up -d
```

All services start successfully and communicate through the logging network.

---

## Task 2: Integrate Your Applications (3 pts)

### Application with JSON Logging

The Flask application was updated to output structured JSON logs. A custom JSONFormatter class extends the standard logging module:

```python
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName
        }
        # Add request context if available
        if hasattr(record, 'method'):
            log_record['method'] = record.method
        if hasattr(record, 'path'):
            log_record['path'] = record.path
        if hasattr(record, 'status'):
            log_record['status'] = record.status
        return json.dumps(log_record)
```

### Request Logging

Middleware captures all HTTP requests:

```python
@app.before_request
def log_request_start():
    request.start_time = time.time()
    logger.info('Request started', extra={
        'method': request.method,
        'path': request.path,
        'ip': request.remote_addr
    })

@app.after_request
def log_request_end(response):
    duration = time.time() - request.start_time
    logger.info('Request completed', extra={
        'method': request.method,
        'path': request.path,
        'status': response.status_code,
        'duration': round(duration, 3)
    })
    return response
```

### Log Generation

Traffic was generated to populate logs:

```bash
for i in {1..20}; do
  curl http://localhost:5000/
  curl http://localhost:5000/health
  sleep 0.5
done
```

Example log output:
```json
{"timestamp": "2026-03-12T14:30:45.123Z", "level": "INFO", "message": "Request completed", "method": "GET", "path": "/", "status": 200, "duration": 0.045}
```

---

## Task 3: Build Log Dashboard (2 pts)

### LogQL Queries

Several LogQL queries were developed for different purposes:

| Query | Purpose |
|-------|---------|
| `{app="devops-python"}` | All logs from the application |
| `{app="devops-python"} |= "/health"` | Health check logs only |
| `rate({app="devops-python"}[1m])` | Request rate per second |
| `count_over_time({app="devops-python"}[5m])` | Log volume over 5 minutes |
| `{app="devops-python"} | json | level="ERROR"` | Only error logs with JSON parsing |

### Dashboard Panels

The dashboard consists of 4 panels:

**Panel 1: Recent Logs**
- Type: Logs visualization
- Query: `{app="devops-python"}`
- Shows the most recent log entries from the application

**Panel 2: Request Rate**
- Type: Time series graph
- Query: `rate({app="devops-python"}[1m])`
- Displays requests per second over time

**Panel 3: Health Checks**
- Type: Logs visualization
- Query: `{app="devops-python"} |= "/health"`
- Shows only health check endpoint logs

**Panel 4: Log Count**
- Type: Stat visualization
- Query: `count_over_time({app="devops-python"}[5m])`
- Displays total log count in the last 5 minutes

All panels use data from the Loki data source and update in real-time.

---

## Task 4: Production Readiness (1 pt)

### Resource Limits

Each service has resource constraints to prevent resource exhaustion:

```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
    reservations:
      cpus: '0.25'
      memory: 256M
```

### Health Checks

Health checks ensure services are functioning correctly:

- **Loki**: Checks `/ready` endpoint
- **Grafana**: Checks `/api/health` endpoint
- **app-python**: Checks `/health` endpoint

### Security

Grafana security was enhanced:
- Anonymous access disabled (`GF_AUTH_ANONYMOUS_ENABLED=false`)
- Admin password stored in `.env` file
- `.env` added to `.gitignore` to prevent committing secrets

### Data Retention

Loki is configured with 7-day retention:
```yaml
limits_config:
  retention_period: 168h
```

---

## LogQL Query Examples

### Basic Stream Selection
```logql
{app="devops-python"}
```

### Text Filtering
```logql
{app="devops-python"} |= "ERROR"
{app="devops-python"} != "health"
```

### JSON Parsing
```logql
{app="devops-python"} | json | level="INFO" | method="GET"
```

### Metrics from Logs
```logql
rate({app="devops-python"}[5m])
sum by (level) (count_over_time({app="devops-python"} | json [5m]))
```

### Time Range Queries
```logql
{app="devops-python"} |= "ERROR" | json | status=500
```

---

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Loki 3.0 configuration differences | Updated compactor config, removed deprecated fields |
| Promtail connection refused | Added depends_on and health checks for proper startup order |
| Python externally-managed environment | Switched from pip to apt packages (python3-docker) |
| Port conflict with old container | Removed stale devops-app container |
| Browser cannot connect to localhost | Used 127.0.0.1 instead of localhost |
| JSON logs not parsing | Implemented custom JSONFormatter in Flask app |

---

## Summary

This lab successfully deployed a complete logging stack with Loki, Promtail, and Grafana. The Python application was enhanced with structured JSON logging. A comprehensive dashboard was created with four panels showing different aspects of application logs. Production-ready features including resource limits, health checks, and security were implemented.

**Key Learnings:**
- Loki 3.0 uses TSDB for improved performance
- Promtail discovers containers via Docker socket
- LogQL provides powerful log querying capabilities
- Structured logging (JSON) enables better log analysis
- Grafana dashboards centralize log visualization

**Time Spent:** 6 hours

**Most Difficult Part:** Configuring Loki correctly for version 3.0 and debugging the Python environment issues on Ubuntu 24.04.
```