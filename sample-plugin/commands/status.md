---
name: status
description: Check the status of your CI/CD pipelines, deployments, and infrastructure
category: monitoring
aliases: [st, stat]
parameters:
  - name: service
    type: string
    description: "Specific service to check (optional)"
    required: false
    default: "all"
  - name: environment
    type: string
    description: "Target environment (dev, staging, prod)"
    required: false
    default: "all"
  - name: format
    type: string
    description: "Output format (json, table, summary)"
    required: false
    default: "summary"
---

# Status Command

## Description
The `status` command provides comprehensive status information about your DevOps infrastructure, including:
- CI/CD pipeline status
- Deployment health checks
- Container and orchestration status
- Database connectivity
- Service availability
- Resource utilization

## Usage Examples

### Basic Status Check
```bash
@devops status
```

### Check Specific Service
```bash
@devops status --service api-gateway
```

### Production Environment Status
```bash
@devops status --environment prod --format json
```

## Implementation

When this command is invoked, Claude will:

1. **Gather System Information**
   - Check running processes and services
   - Query container orchestration platforms (Kubernetes, Docker)
   - Verify database connections
   - Check API endpoints

2. **Analyze Health Metrics**
   - CPU and memory utilization
   - Disk space availability
   - Network connectivity
   - Application response times

3. **Generate Status Report**
   - Compile findings into requested format
   - Highlight any issues or warnings
   - Provide recommendations for improvements

## Response Template

```markdown
## DevOps Infrastructure Status Report

### 🟢 Overall Health: {status}

#### CI/CD Pipelines
- Build Pipeline: {status}
- Test Pipeline: {status}
- Deploy Pipeline: {status}
- Last successful build: {timestamp}

#### Services Status
| Service | Status | Health | Uptime | Response Time |
|---------|--------|--------|---------|---------------|
| API Gateway | 🟢 Running | 100% | 99.9% | 45ms |
| Database | 🟢 Running | 100% | 99.99% | 12ms |
| Cache | 🟢 Running | 100% | 99.95% | 2ms |

#### Environment Health
- **Development**: All systems operational
- **Staging**: All systems operational
- **Production**: All systems operational

#### Resource Utilization
- CPU: {percentage}% utilized
- Memory: {used}GB / {total}GB
- Disk: {used}GB / {total}GB
- Network: {bandwidth} Mbps

#### Recent Alerts
{list of recent alerts if any}

#### Recommendations
{list of optimization suggestions}
```

## Error Handling

The command handles various error scenarios:
- Service unreachable: Provides fallback status from cache
- Authentication failures: Prompts for credentials
- Timeout errors: Reports partial status with warnings
- Configuration issues: Suggests fixes

## Integration Points

This command integrates with:
- Kubernetes API
- Docker daemon
- CI/CD platforms (Jenkins, GitHub Actions, GitLab CI)
- Monitoring tools (Prometheus, Grafana)
- Cloud providers (AWS, Azure, GCP)
- Database systems
- Message queues
