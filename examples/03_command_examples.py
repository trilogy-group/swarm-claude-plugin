#!/usr/bin/env python3
"""
Claude DevOps Plugin - Command Examples
Demonstrates the usage of plugin commands: status and logs
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum


class CommandExecutor:
    """Executor for Claude plugin commands"""
    
    def __init__(self, plugin_name: str = "devops-assistant"):
        self.plugin_name = plugin_name
        self.command_prefix = "devops"
        self.command_history = []
    
    def execute(self, command: str, params: Dict = None) -> Dict:
        """Execute a plugin command"""
        execution_time = datetime.now()
        
        # Log command
        self.command_history.append({
            "timestamp": execution_time.isoformat(),
            "command": command,
            "params": params
        })
        
        # Execute command
        if command == "status":
            result = self._execute_status(params or {})
        elif command == "logs":
            result = self._execute_logs(params or {})
        else:
            result = {"error": f"Unknown command: {command}"}
        
        # Print formatted output
        self._print_result(command, params, result)
        
        return result
    
    def _execute_status(self, params: Dict) -> Dict:
        """Execute status command with various parameters"""
        service = params.get("service", "all")
        environment = params.get("environment", "all")
        format_type = params.get("format", "summary")
        
        # Generate status data
        status_data = {
            "timestamp": datetime.now().isoformat(),
            "environment": environment,
            "overall_health": "healthy",
            "services": self._get_service_status(service),
            "infrastructure": self._get_infrastructure_status(),
            "deployments": self._get_deployment_status(environment),
            "alerts": self._get_active_alerts(),
            "metrics": self._get_system_metrics()
        }
        
        # Format based on requested format
        if format_type == "json":
            return status_data
        elif format_type == "table":
            return self._format_as_table(status_data)
        else:  # summary
            return self._format_as_summary(status_data)
    
    def _execute_logs(self, params: Dict) -> Dict:
        """Execute logs command with various filters"""
        filter_type = params.get("filter", None)
        since = params.get("since", "1 hour ago")
        tail = params.get("tail", 100)
        follow = params.get("follow", False)
        service = params.get("service", None)
        
        # Parse time range
        start_time = self._parse_time(since)
        
        # Generate log entries
        all_logs = self._generate_log_entries(start_time)
        
        # Apply filters
        filtered_logs = self._filter_logs(all_logs, filter_type, service)
        
        # Limit to tail count
        if tail and not follow:
            filtered_logs = filtered_logs[-tail:]
        
        return {
            "logs": filtered_logs,
            "total_count": len(filtered_logs),
            "time_range": {
                "start": start_time.isoformat(),
                "end": datetime.now().isoformat()
            },
            "filters_applied": {
                "level": filter_type,
                "service": service,
                "tail": tail
            },
            "follow_mode": follow
        }
    
    def _get_service_status(self, service: str) -> Dict:
        """Get status for specific service or all services"""
        all_services = {
            "api-gateway": {
                "status": "running",
                "health": "healthy",
                "version": "v2.4.1",
                "uptime": "48h 23m",
                "cpu": "45%",
                "memory": "2.3GB",
                "requests_per_min": 1250,
                "error_rate": "0.02%"
            },
            "auth-service": {
                "status": "running",
                "health": "healthy",
                "version": "v1.8.3",
                "uptime": "120h 45m",
                "cpu": "23%",
                "memory": "512MB",
                "active_sessions": 3421,
                "auth_rate": "99.8%"
            },
            "database": {
                "status": "running",
                "health": "healthy",
                "version": "PostgreSQL 14.5",
                "uptime": "720h",
                "connections": 45,
                "queries_per_sec": 892,
                "replication_lag": "0.3s",
                "disk_usage": "67GB"
            },
            "cache": {
                "status": "running",
                "health": "degraded",
                "version": "Redis 6.2",
                "uptime": "24h 10m",
                "memory": "4.2GB",
                "hit_rate": "87%",
                "eviction_rate": "12/min",
                "issue": "High memory usage"
            },
            "message-queue": {
                "status": "running",
                "health": "healthy",
                "version": "RabbitMQ 3.9",
                "uptime": "240h",
                "messages_queued": 1234,
                "messages_per_min": 450,
                "consumers": 12
            }
        }
        
        if service == "all":
            return all_services
        elif service in all_services:
            return {service: all_services[service]}
        else:
            return {"error": f"Service '{service}' not found"}
    
    def _get_infrastructure_status(self) -> Dict:
        """Get infrastructure status"""
        return {
            "clusters": {
                "production": {
                    "nodes": 12,
                    "cpu_utilization": "68%",
                    "memory_utilization": "72%",
                    "pods_running": 145,
                    "pods_pending": 2
                },
                "staging": {
                    "nodes": 4,
                    "cpu_utilization": "45%",
                    "memory_utilization": "51%",
                    "pods_running": 48,
                    "pods_pending": 0
                }
            },
            "load_balancers": {
                "main-lb": {
                    "status": "active",
                    "backends_healthy": 8,
                    "backends_unhealthy": 0,
                    "requests_per_sec": 2500
                }
            },
            "storage": {
                "primary": {
                    "used": "2.4TB",
                    "available": "5.6TB",
                    "iops": 15000
                }
            }
        }
    
    def _get_deployment_status(self, environment: str) -> Dict:
        """Get deployment status"""
        return {
            "latest_deployment": {
                "version": "v2.4.1",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "status": "successful",
                "duration": "12m 34s",
                "deployed_by": "ci-bot"
            },
            "previous_deployments": [
                {
                    "version": "v2.4.0",
                    "timestamp": (datetime.now() - timedelta(days=2)).isoformat(),
                    "status": "successful"
                },
                {
                    "version": "v2.3.9",
                    "timestamp": (datetime.now() - timedelta(days=5)).isoformat(),
                    "status": "rolled_back"
                }
            ],
            "pending_deployments": [],
            "deployment_frequency": "3 per week",
            "rollback_count": 1
        }
    
    def _get_active_alerts(self) -> List[Dict]:
        """Get active alerts"""
        return [
            {
                "id": "ALERT-001",
                "severity": "warning",
                "service": "cache",
                "message": "High memory usage detected (>80%)",
                "triggered_at": (datetime.now() - timedelta(minutes=30)).isoformat(),
                "acknowledged": False
            }
        ]
    
    def _get_system_metrics(self) -> Dict:
        """Get system metrics"""
        return {
            "availability": "99.98%",
            "avg_response_time": "145ms",
            "error_rate": "0.02%",
            "throughput": "2500 req/s",
            "active_users": 12453
        }
    
    def _generate_log_entries(self, start_time: datetime) -> List[Dict]:
        """Generate sample log entries"""
        log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
        services = ["api-gateway", "auth-service", "database", "cache"]
        
        logs = []
        current_time = start_time
        
        # Generate diverse log entries
        log_templates = [
            ("INFO", "Application started successfully"),
            ("INFO", "Health check passed"),
            ("INFO", "Request processed successfully"),
            ("WARNING", "High memory usage detected"),
            ("WARNING", "Slow query detected"),
            ("ERROR", "Connection timeout to database"),
            ("ERROR", "Authentication failed for user"),
            ("DEBUG", "Cache miss for key"),
            ("INFO", "Deployment completed"),
            ("WARNING", "Rate limit approaching for client")
        ]
        
        for i in range(150):  # Generate 150 log entries
            template = log_templates[i % len(log_templates)]
            logs.append({
                "timestamp": current_time.isoformat(),
                "level": template[0],
                "service": services[i % len(services)],
                "message": f"{template[1]} #{i}",
                "details": {
                    "request_id": f"req-{i:04d}",
                    "user_id": f"user-{i % 100:03d}" if i % 3 == 0 else None,
                    "duration_ms": 50 + (i * 10) % 500
                }
            })
            current_time += timedelta(seconds=30)
        
        return logs
    
    def _filter_logs(self, logs: List[Dict], filter_type: str, service: str) -> List[Dict]:
        """Filter logs based on criteria"""
        filtered = logs
        
        if filter_type:
            if filter_type.lower() == "error":
                filtered = [log for log in filtered if log["level"] == "ERROR"]
            elif filter_type.lower() == "warning":
                filtered = [log for log in filtered if log["level"] in ["WARNING", "ERROR"]]
            elif filter_type.lower() == "info":
                filtered = [log for log in filtered if log["level"] == "INFO"]
        
        if service:
            filtered = [log for log in filtered if log["service"] == service]
        
        return filtered
    
    def _parse_time(self, time_str: str) -> datetime:
        """Parse relative time string"""
        now = datetime.now()
        
        if "hour" in time_str:
            hours = int(time_str.split()[0]) if time_str.split()[0].isdigit() else 1
            return now - timedelta(hours=hours)
        elif "day" in time_str:
            days = int(time_str.split()[0]) if time_str.split()[0].isdigit() else 1
            return now - timedelta(days=days)
        elif "minute" in time_str:
            minutes = int(time_str.split()[0]) if time_str.split()[0].isdigit() else 1
            return now - timedelta(minutes=minutes)
        else:
            return now - timedelta(hours=1)  # Default to 1 hour
    
    def _format_as_table(self, data: Dict) -> Dict:
        """Format status data as table"""
        return {
            "format": "table",
            "content": data,
            "display_hint": "Use tabulate or similar library for rendering"
        }
    
    def _format_as_summary(self, data: Dict) -> Dict:
        """Format status data as summary"""
        healthy_services = sum(
            1 for s in data["services"].values() 
            if isinstance(s, dict) and s.get("health") == "healthy"
        )
        total_services = len(data["services"])
        
        return {
            "format": "summary",
            "summary": {
                "overall_status": data["overall_health"],
                "healthy_services": f"{healthy_services}/{total_services}",
                "active_alerts": len(data["alerts"]),
                "last_deployment": data["deployments"]["latest_deployment"]["version"],
                "system_metrics": data["metrics"]
            }
        }
    
    def _print_result(self, command: str, params: Dict, result: Dict):
        """Print formatted command result"""
        print(f"\n{'='*60}")
        print(f"Command: @{self.command_prefix} {command}")
        if params:
            print(f"Parameters: {json.dumps(params, indent=2)}")
        print(f"{'='*60}")
        
        if command == "status":
            self._print_status_result(result)
        elif command == "logs":
            self._print_logs_result(result)
    
    def _print_status_result(self, result: Dict):
        """Print status command result"""
        if "summary" in result:
            summary = result["summary"]
            print("\n📊 System Status Summary:")
            print(f"  Overall Status: {summary['overall_status']}")
            print(f"  Healthy Services: {summary['healthy_services']}")
            print(f"  Active Alerts: {summary['active_alerts']}")
            print(f"  Latest Deployment: {summary['last_deployment']}")
            print("\n📈 System Metrics:")
            for key, value in summary['system_metrics'].items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
        else:
            print(json.dumps(result, indent=2))
    
    def _print_logs_result(self, result: Dict):
        """Print logs command result"""
        print(f"\n📜 Log Entries ({result['total_count']} total):")
        print(f"Time Range: {result['time_range']['start']} to {result['time_range']['end']}")
        
        if result['filters_applied']['level']:
            print(f"Filter: {result['filters_applied']['level']}")
        
        print("\nRecent Logs:")
        for log in result['logs'][-5:]:  # Show last 5 entries
            level_icon = {
                "INFO": "ℹ️",
                "WARNING": "⚠️",
                "ERROR": "❌",
                "DEBUG": "🔧"
            }.get(log['level'], "📝")
            
            print(f"{level_icon} [{log['timestamp']}] {log['service']}: {log['message']}")


# Example usage functions
def example_status_commands():
    """Demonstrate various status command usages"""
    print("\n" + "="*70)
    print("STATUS COMMAND EXAMPLES")
    print("="*70)
    
    executor = CommandExecutor()
    
    # Example 1: Basic status
    print("\n1️⃣ Basic Status Check")
    executor.execute("status")
    
    # Example 2: Status for specific service
    print("\n2️⃣ Service-Specific Status")
    executor.execute("status", {"service": "database"})
    
    # Example 3: Status for specific environment
    print("\n3️⃣ Environment-Specific Status")
    executor.execute("status", {"environment": "production"})
    
    # Example 4: JSON formatted status
    print("\n4️⃣ JSON Formatted Status")
    result = executor.execute("status", {"format": "json", "service": "api-gateway"})
    
    return executor.command_history


def example_logs_commands():
    """Demonstrate various logs command usages"""
    print("\n" + "="*70)
    print("LOGS COMMAND EXAMPLES")
    print("="*70)
    
    executor = CommandExecutor()
    
    # Example 1: Recent logs
    print("\n1️⃣ Recent Logs (Default)")
    executor.execute("logs")
    
    # Example 2: Error logs only
    print("\n2️⃣ Error Logs Only")
    executor.execute("logs", {"filter": "error"})
    
    # Example 3: Logs from specific service
    print("\n3️⃣ Service-Specific Logs")
    executor.execute("logs", {"service": "auth-service", "tail": 20})
    
    # Example 4: Logs with time range
    print("\n4️⃣ Logs from Last 2 Hours")
    executor.execute("logs", {"since": "2 hours ago", "filter": "warning"})
    
    # Example 5: Follow mode simulation
    print("\n5️⃣ Follow Mode (Live Tail)")
    executor.execute("logs", {"follow": True, "tail": 10})
    
    return executor.command_history


def example_combined_workflow():
    """Demonstrate combined command workflow"""
    print("\n" + "="*70)
    print("COMBINED WORKFLOW EXAMPLE: Health Check & Troubleshooting")
    print("="*70)
    
    executor = CommandExecutor()
    
    # Step 1: Check overall status
    print("\n📍 Step 1: Check Overall System Status")
    status_result = executor.execute("status", {"format": "summary"})
    
    # Step 2: If there are alerts, check specific service
    if status_result.get("summary", {}).get("active_alerts", 0) > 0:
        print("\n📍 Step 2: Detected Alerts - Checking Problem Service")
        executor.execute("status", {"service": "cache"})
        
        # Step 3: Check error logs for the service
        print("\n📍 Step 3: Checking Error Logs for Problem Service")
        executor.execute("logs", {
            "service": "cache",
            "filter": "error",
            "since": "1 hour ago",
            "tail": 20
        })
        
        # Step 4: Check warning logs for patterns
        print("\n📍 Step 4: Checking Warning Logs for Patterns")
        executor.execute("logs", {
            "service": "cache",
            "filter": "warning",
            "since": "3 hours ago",
            "tail": 30
        })
    
    print("\n✅ Workflow completed - Issue identified and logs collected")
    
    return executor.command_history


def example_monitoring_dashboard():
    """Simulate a monitoring dashboard using commands"""
    print("\n" + "="*70)
    print("MONITORING DASHBOARD SIMULATION")
    print("="*70)
    
    executor = CommandExecutor()
    
    # Dashboard sections
    sections = [
        ("🏠 Infrastructure Overview", {"format": "summary"}),
        ("🔧 Service Health", {"service": "all", "format": "json"}),
        ("📊 Performance Metrics", {"environment": "production"}),
        ("🚨 Recent Errors", {"filter": "error", "tail": 5}),
        ("⚠️ Recent Warnings", {"filter": "warning", "tail": 5})
    ]
    
    dashboard_data = {}
    
    for title, params in sections:
        print(f"\n{title}")
        if "filter" in params:
            result = executor.execute("logs", params)
            dashboard_data[title] = result
        else:
            result = executor.execute("status", params)
            dashboard_data[title] = result
    
    # Summary
    print("\n" + "="*70)
    print("DASHBOARD SUMMARY")
    print("="*70)
    
    # Calculate metrics
    total_errors = sum(
        1 for section in dashboard_data.values() 
        if "logs" in section 
        for log in section["logs"] 
        if log.get("level") == "ERROR"
    )
    
    print(f"📈 Dashboard Refresh: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"❌ Total Errors: {total_errors}")
    print(f"✅ System Health: {'Healthy' if total_errors < 5 else 'Degraded'}")
    
    return dashboard_data


def example_cicd_integration():
    """Example of using commands in CI/CD pipeline"""
    print("\n" + "="*70)
    print("CI/CD PIPELINE INTEGRATION EXAMPLE")
    print("="*70)
    
    executor = CommandExecutor()
    pipeline_status = "success"
    
    # Pre-deployment checks
    print("\n🔄 PRE-DEPLOYMENT CHECKS")
    print("-" * 40)
    
    # Check production status
    print("\n1. Checking Production Status...")
    prod_status = executor.execute("status", {
        "environment": "production",
        "format": "json"
    })
    
    if prod_status.get("overall_health") != "healthy":
        print("  ❌ Production is not healthy - Deployment blocked")
        pipeline_status = "failed"
    else:
        print("  ✅ Production is healthy")
    
    # Check for recent errors
    print("\n2. Checking for Recent Errors...")
    error_logs = executor.execute("logs", {
        "filter": "error",
        "since": "30 minutes ago",
        "tail": 10
    })
    
    if error_logs["total_count"] > 5:
        print(f"  ⚠️ Found {error_logs['total_count']} errors in last 30 minutes")
        pipeline_status = "warning"
    else:
        print("  ✅ Error rate is acceptable")
    
    # Check service dependencies
    print("\n3. Checking Service Dependencies...")
    services_to_check = ["database", "cache", "message-queue"]
    
    for service in services_to_check:
        service_status = executor.execute("status", {"service": service})
        service_health = next(iter(service_status["services"].values()))["health"]
        
        if service_health != "healthy":
            print(f"  ❌ {service}: {service_health}")
            if service_health == "down":
                pipeline_status = "failed"
        else:
            print(f"  ✅ {service}: healthy")
    
    # Final decision
    print("\n" + "="*40)
    if pipeline_status == "success":
        print("✅ DEPLOYMENT APPROVED - All checks passed")
    elif pipeline_status == "warning":
        print("⚠️ DEPLOYMENT WARNING - Proceed with caution")
    else:
        print("❌ DEPLOYMENT BLOCKED - Critical issues detected")
    
    return {
        "pipeline_status": pipeline_status,
        "checks_performed": len(executor.command_history),
        "timestamp": datetime.now().isoformat()
    }


def main():
    """Main function to run all command examples"""
    print("╔" + "="*68 + "╗")
    print("║" + " "*20 + "CLAUDE COMMAND EXAMPLES" + " "*24 + "║")
    print("║" + " "*15 + "Demonstrating Status and Logs Commands" + " "*14 + "║")
    print("╚" + "="*68 + "╝")
    
    # Run examples
    status_history = example_status_commands()
    logs_history = example_logs_commands()
    workflow_history = example_combined_workflow()
    dashboard_data = example_monitoring_dashboard()
    cicd_result = example_cicd_integration()
    
    # Summary
    print("\n" + "="*70)
    print("EXECUTION SUMMARY")
    print("="*70)
    print("✅ All command examples completed successfully")
    print(f"📊 Total commands executed: {len(status_history) + len(logs_history)}")
    print("\nCommands demonstrated:")
    print("  • @devops status - Infrastructure and service status")
    print("  • @devops logs - Log retrieval and filtering")
    print("\nUse cases covered:")
    print("  • Basic status checks")
    print("  • Service-specific monitoring")
    print("  • Log filtering and analysis")
    print("  • Troubleshooting workflows")
    print("  • Dashboard simulation")
    print("  • CI/CD integration")
    
    # Save results
    results = {
        "status_examples": status_history,
        "logs_examples": logs_history,
        "workflow": workflow_history,
        "dashboard": dashboard_data,
        "cicd": cicd_result
    }
    
    with open("command_demo_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print("\n📁 Results saved to command_demo_results.json")
    
    return results


if __name__ == "__main__":
    main()
