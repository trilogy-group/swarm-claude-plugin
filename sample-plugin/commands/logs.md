---
name: logs
description: Retrieve and analyze logs from various services and environments
category: monitoring
aliases: [log, tail]
parameters:
  - name: service
    type: string
    description: "Service name to fetch logs from"
    required: true
  - name: lines
    type: number
    description: "Number of log lines to retrieve"
    required: false
    default: 100
  - name: follow
    type: boolean
    description: "Follow log output in real-time"
    required: false
    default: false
  - name: filter
    type: string
    description: "Filter pattern for log entries"
    required: false
  - name: level
    type: string
    description: "Log level filter (ERROR, WARN, INFO, DEBUG)"
    required: false
    default: "ALL"
  - name: timeframe
    type: string
    description: "Time range (e.g., '1h', '24h', '7d')"
    required: false
    default: "1h"
---

# Logs Command

## Description
The `logs` command provides powerful log retrieval and analysis capabilities for debugging and monitoring your applications and infrastructure.

## Features
- Real-time log streaming
- Advanced filtering and pattern matching
- Multi-service log aggregation
- Log level filtering
- Time-based queries
- Error pattern detection
- Performance analysis from logs

## Usage Examples

### View Recent Logs
```bash
@devops logs --service api-gateway
```

### Follow Logs in Real-time
```bash
@devops logs --service api-gateway --follow
```

### Filter Error Logs
```bash
@devops logs --service api-gateway --level ERROR --timeframe 24h
```

### Search with Pattern
```bash
@devops logs --service api-gateway --filter "user authentication failed"
```

### Tail Specific Number of Lines
```bash
@devops logs --service database --lines 500 --level WARN
```

## Implementation Logic

### 1. Log Source Detection
Claude will automatically detect and connect to appropriate log sources:
- Container logs (Docker, Kubernetes)
- Application log files
- Cloud logging services (CloudWatch, Stackdriver, Azure Monitor)
- System logs (syslog, journalctl)
- Database logs
- Web server logs

### 2. Log Processing Pipeline
```
1. Connect to log source
2. Apply time range filter
3. Apply log level filter
4. Apply custom pattern filter
5. Format and highlight output
6. Stream or batch return results
```

### 3. Intelligent Analysis
Claude performs automatic analysis:
- Error pattern recognition
- Performance bottleneck detection
- Security event identification
- Anomaly detection
- Correlation across services

## Response Format

### Standard Log Output
```
[2024-01-15 10:23:45] [INFO] api-gateway: Request received from 192.168.1.100
[2024-01-15 10:23:45] [INFO] api-gateway: Authentication successful for user: john.doe
[2024-01-15 10:23:46] [ERROR] api-gateway: Database connection timeout
[2024-01-15 10:23:46] [WARN] api-gateway: Retrying database connection (attempt 1/3)
[2024-01-15 10:23:47] [INFO] api-gateway: Database connection restored
```

### Analysis Summary
```markdown
## Log Analysis Summary

### Overview
- **Time Range**: Last 1 hour
- **Total Entries**: 1,234
- **Error Rate**: 2.3%
- **Warning Rate**: 5.1%

### Error Distribution
| Error Type | Count | Percentage |
|------------|-------|------------|
| Connection Timeout | 15 | 45% |
| Authentication Failed | 10 | 30% |
| Resource Not Found | 8 | 25% |

### Performance Metrics
- Average Response Time: 145ms
- P95 Response Time: 450ms
- P99 Response Time: 1200ms

### Detected Patterns
1. **Spike in connection timeouts** between 10:15-10:20
   - Likely cause: Database maintenance window
   - Recommendation: Implement connection pooling

2. **Authentication failures** from IP: 203.0.113.42
   - Pattern suggests brute force attempt
   - Recommendation: Enable rate limiting

### Critical Events
⚠️ Memory usage exceeded 90% at 10:45
⚠️ Disk space below 10% on node-3
🔴 Service crash detected at 09:30 (auto-recovered)
```

## Advanced Features

### Multi-Service Correlation
```bash
@devops logs --service "api-gateway,database,cache" --filter "transaction-id:abc123"
```

### Export Capabilities
```bash
@devops logs --service api-gateway --format json --export logs-backup.json
```

### Real-time Alerting
When following logs, Claude will:
- Highlight critical errors in red
- Alert on unusual patterns
- Suggest immediate actions for critical issues

## Error Handling

Common error scenarios and responses:
- **No logs available**: Check service status and permissions
- **Access denied**: Verify credentials and permissions
- **Service not found**: List available services with `@devops services`
- **Invalid filter**: Provide filter syntax help
- **Connection timeout**: Attempt alternative log sources

## Integration with Other Commands

Combine with other DevOps commands:
```bash
# Check status then view logs if issues detected
@devops status && @devops logs --service {problematic-service}

# View logs and trigger deployment if stable
@devops logs --service api-gateway --level ERROR --lines 0 && @devops deploy
```
