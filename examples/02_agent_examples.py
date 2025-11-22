#!/usr/bin/env python3
"""
Claude DevOps Plugin - Agent Examples
Demonstrates all 11 agents with realistic use cases
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any


class AgentManager:
    """Manager for plugin agents with simulated Claude SDK integration"""
    
    def __init__(self):
        self.agents = self._initialize_agents()
        self.execution_history = []
    
    def _initialize_agents(self) -> Dict:
        """Initialize all available agents"""
        return {
            "security-reviewer": SecurityReviewerAgent(),
            "performance-tester": PerformanceTesterAgent(),
            "compliance-checker": ComplianceCheckerAgent(),
            "repository-initializer": RepositoryInitializerAgent(),
            "spec-system-prompt-loader": SpecSystemPromptLoaderAgent(),
            "spec-requirements-writer": SpecRequirementsWriterAgent(),
            "design-spec-writer": DesignSpecWriterAgent(),
            "spec-tasks-writer": SpecTasksWriterAgent(),
            "spec-implementer": SpecImplementerAgent(),
            "test-spec-writer": TestSpecWriterAgent(),
            "spec-judge": SpecJudgeAgent()
        }
    
    async def execute(self, agent_name: str, task: str, context: Dict = None) -> Dict:
        """Execute an agent task"""
        if agent_name not in self.agents:
            raise ValueError(f"Unknown agent: {agent_name}")
        
        agent = self.agents[agent_name]
        result = await agent.execute(task, context or {})
        
        # Log execution
        self.execution_history.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "task": task,
            "success": result.get("status") == "success"
        })
        
        return result


class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
    
    async def execute(self, task: str, context: Dict) -> Dict:
        """Execute agent task - to be implemented by subclasses"""
        raise NotImplementedError


class SecurityReviewerAgent(BaseAgent):
    """Security analysis and vulnerability detection"""
    
    def __init__(self):
        super().__init__(
            "security-reviewer",
            ["vulnerability_detection", "dependency_scanning", "secrets_detection", "compliance_checking"]
        )
    
    async def execute(self, task: str, context: Dict) -> Dict:
        print(f"\n🔒 Security Reviewer Agent: {task}")
        await asyncio.sleep(0.5)  # Simulate processing
        
        if "code_review" in task.lower():
            return await self._review_code(context)
        elif "dependency" in task.lower():
            return await self._scan_dependencies(context)
        elif "secrets" in task.lower():
            return await self._detect_secrets(context)
        else:
            return await self._general_security_scan(context)
    
    async def _review_code(self, context: Dict) -> Dict:
        """Review code for security vulnerabilities"""
        return {
            "status": "success",
            "vulnerabilities": [
                {
                    "type": "SQL_INJECTION",
                    "severity": "HIGH",
                    "file": "api/database.py",
                    "line": 42,
                    "description": "User input directly concatenated in SQL query",
                    "recommendation": "Use parameterized queries"
                },
                {
                    "type": "XSS",
                    "severity": "MEDIUM",
                    "file": "templates/user.html",
                    "line": 18,
                    "description": "Unescaped user input in template",
                    "recommendation": "Use template auto-escaping"
                },
                {
                    "type": "WEAK_CRYPTO",
                    "severity": "HIGH",
                    "file": "auth/password.py",
                    "line": 8,
                    "description": "MD5 hash used for passwords",
                    "recommendation": "Use bcrypt or argon2"
                }
            ],
            "summary": {
                "files_scanned": 45,
                "vulnerabilities_found": 3,
                "high_severity": 2,
                "medium_severity": 1,
                "low_severity": 0
            }
        }
    
    async def _scan_dependencies(self, context: Dict) -> Dict:
        """Scan dependencies for known vulnerabilities"""
        return {
            "status": "success",
            "vulnerable_dependencies": [
                {
                    "package": "requests",
                    "current_version": "2.25.0",
                    "safe_version": "2.28.1",
                    "vulnerability": "CVE-2022-12345",
                    "severity": "MEDIUM"
                },
                {
                    "package": "django",
                    "current_version": "3.1.0",
                    "safe_version": "3.2.15",
                    "vulnerability": "CVE-2022-67890",
                    "severity": "HIGH"
                }
            ],
            "total_dependencies": 125,
            "vulnerable_count": 2
        }
    
    async def _detect_secrets(self, context: Dict) -> Dict:
        """Detect hardcoded secrets and credentials"""
        return {
            "status": "success",
            "secrets_found": [
                {
                    "type": "API_KEY",
                    "file": "config/settings.py",
                    "line": 15,
                    "pattern": "sk_live_*",
                    "recommendation": "Use environment variables"
                },
                {
                    "type": "DATABASE_PASSWORD",
                    "file": "config/database.yml",
                    "line": 8,
                    "recommendation": "Use secrets management system"
                }
            ],
            "files_scanned": 250,
            "secrets_count": 2
        }
    
    async def _general_security_scan(self, context: Dict) -> Dict:
        """General security scan"""
        return {
            "status": "success",
            "security_score": 78,
            "issues": 5,
            "recommendations": [
                "Enable 2FA for all admin accounts",
                "Update TLS configuration to 1.3",
                "Implement rate limiting on API endpoints"
            ]
        }


class PerformanceTesterAgent(BaseAgent):
    """Performance testing and analysis"""
    
    def __init__(self):
        super().__init__(
            "performance-tester",
            ["load_testing", "stress_testing", "benchmark_analysis", "bottleneck_detection"]
        )
    
    async def execute(self, task: str, context: Dict) -> Dict:
        print(f"\n⚡ Performance Tester Agent: {task}")
        await asyncio.sleep(0.5)
        
        if "load" in task.lower():
            return await self._load_test(context)
        elif "stress" in task.lower():
            return await self._stress_test(context)
        elif "benchmark" in task.lower():
            return await self._benchmark(context)
        else:
            return await self._analyze_performance(context)
    
    async def _load_test(self, context: Dict) -> Dict:
        """Run load testing"""
        return {
            "status": "success",
            "test_configuration": {
                "concurrent_users": context.get("users", 100),
                "duration": context.get("duration", "5m"),
                "ramp_up": "30s"
            },
            "results": {
                "avg_response_time": 145,
                "p50_response_time": 120,
                "p95_response_time": 450,
                "p99_response_time": 890,
                "requests_per_second": 1250,
                "error_rate": 0.02,
                "success_rate": 99.98
            },
            "bottlenecks": [
                "Database connection pool limit reached",
                "CPU usage peaked at 95%"
            ]
        }
    
    async def _stress_test(self, context: Dict) -> Dict:
        """Run stress testing"""
        return {
            "status": "success",
            "breaking_point": {
                "concurrent_users": 5000,
                "requests_per_second": 8500,
                "response_time": 5000
            },
            "failure_mode": "Database connection timeout",
            "recovery_time": "45 seconds"
        }
    
    async def _benchmark(self, context: Dict) -> Dict:
        """Run performance benchmarks"""
        return {
            "status": "success",
            "benchmarks": {
                "api_endpoint_latency": {
                    "/api/users": 45,
                    "/api/products": 67,
                    "/api/orders": 120
                },
                "database_query_time": {
                    "select_users": 12,
                    "insert_order": 34,
                    "complex_join": 156
                },
                "memory_usage": {
                    "baseline": "512MB",
                    "peak": "2.3GB",
                    "average": "890MB"
                }
            }
        }
    
    async def _analyze_performance(self, context: Dict) -> Dict:
        """Analyze general performance"""
        return {
            "status": "success",
            "performance_score": 85,
            "recommendations": [
                "Implement Redis caching for frequently accessed data",
                "Optimize database indexes",
                "Consider horizontal scaling for API servers"
            ]
        }


class ComplianceCheckerAgent(BaseAgent):
    """Compliance and standards validation"""
    
    def __init__(self):
        super().__init__(
            "compliance-checker",
            ["policy_validation", "standards_checking", "audit_logging", "certification_prep"]
        )
    
    async def execute(self, task: str, context: Dict) -> Dict:
        print(f"\n📋 Compliance Checker Agent: {task}")
        await asyncio.sleep(0.5)
        
        standards = context.get("standards", ["SOC2", "ISO27001", "GDPR"])
        
        return {
            "status": "success",
            "compliance_status": {
                standard: self._check_standard(standard) 
                for standard in standards
            },
            "overall_compliance": 92,
            "issues": [
                {
                    "standard": "GDPR",
                    "requirement": "Data retention policy",
                    "status": "non-compliant",
                    "action": "Update data retention to 90 days"
                }
            ],
            "recommendations": [
                "Implement audit log retention for 7 years",
                "Add data encryption at rest",
                "Update privacy policy with cookie consent"
            ]
        }
    
    def _check_standard(self, standard: str) -> Dict:
        """Check compliance for a specific standard"""
        compliance_scores = {
            "SOC2": 95,
            "ISO27001": 88,
            "GDPR": 91,
            "HIPAA": 78,
            "PCI-DSS": 93
        }
        return {
            "score": compliance_scores.get(standard, 85),
            "status": "compliant" if compliance_scores.get(standard, 85) > 80 else "non-compliant"
        }


class RepositoryInitializerAgent(BaseAgent):
    """Repository creation and initialization from templates"""
    
    def __init__(self):
        super().__init__(
            "repository-initializer",
            ["repo_creation", "template_application", "branch_setup", "ci_cd_config"]
        )
    
    async def execute(self, task: str, context: Dict) -> Dict:
        print(f"\n🚀 Repository Initializer Agent: {task}")
        await asyncio.sleep(0.5)
        
        repo_name = context.get("repo_name", "new-service")
        template = context.get("template", "api-boilerplate")
        
        return {
            "status": "success",
            "repository": {
                "name": repo_name,
                "url": f"https://github.com/your-org/{repo_name}",
                "template_used": template,
                "visibility": "private"
            },
            "initialization": {
                "branches_created": ["main", "develop", "staging"],
                "default_branch": "main",
                "protection_rules": {
                    "main": ["require_pr", "require_reviews", "dismiss_stale_reviews"],
                    "staging": ["require_pr"]
                }
            },
            "configurations": {
                "ci_cd": ".github/workflows/ci.yml",
                "docker": "Dockerfile",
                "kubernetes": "k8s/deployment.yaml",
                "readme": "README.md updated"
            },
            "customizations": [
                f"Updated project name to {repo_name}",
                "Configured environment variables",
                "Set up secrets in GitHub",
                "Created initial documentation"
            ],
            "initial_commit": {
                "sha": "a1b2c3d4e5f6",
                "message": f"Initial setup of {repo_name} from {template}",
                "author": "DevOps Bot"
            }
        }


class SpecSystemPromptLoaderAgent(BaseAgent):
    """Spec workflow system prompt initialization"""
    
    def __init__(self):
        super().__init__(
            "spec-system-prompt-loader",
            ["workflow_initialization", "prompt_loading", "context_setup"]
        )
    
    async def execute(self, task: str, context: Dict) -> Dict:
        print(f"\n📚 Spec System Prompt Loader Agent: {task}")
        await asyncio.sleep(0.3)
        
        workflow_type = context.get("workflow_type", "feature_development")
        
        return {
            "status": "success",
            "workflow": {
                "type": workflow_type,
                "version": "2.0",
                "loaded_prompts": [
                    "requirements_generation",
                    "design_creation",
                    "task_breakdown",
                    "implementation_guidance",
                    "test_generation"
                ]
            },
            "configuration": {
                "requirements_syntax": "EARS",
                "design_patterns": ["Repository", "Factory", "Observer"],
                "test_framework": "pytest",
                "documentation_format": "markdown"
            },
            "context_initialized": True,
            "ready_for_phases": [
                "requirements",
                "design",
                "tasks",
                "implementation",
                "testing",
                "evaluation"
            ]
        }


class SpecRequirementsWriterAgent(BaseAgent):
    """Requirements document generation using EARS syntax"""
    
    def __init__(self):
        super().__init__(
            "spec-requirements-writer",
            ["requirements_generation", "EARS_syntax", "traceability", "validation"]
        )
    
    async def execute(self, task: str, context: Dict) -> Dict:
        print(f"\n📝 Spec Requirements Writer Agent: {task}")
        await asyncio.sleep(0.5)
        
        feature = context.get("feature", "User Authentication")
        
        return {
            "status": "success",
            "document": f"requirements_{feature.lower().replace(' ', '_')}_v1.0.md",
            "requirements": [
                {
                    "id": "REQ-AUTH-001",
                    "type": "functional",
                    "priority": "HIGH",
                    "statement": "WHEN a user submits valid credentials THEN the system SHALL authenticate the user AND generate a JWT token",
                    "acceptance_criteria": [
                        "Valid credentials return 200 status",
                        "JWT token contains user ID and roles",
                        "Token expires in 24 hours"
                    ]
                },
                {
                    "id": "REQ-AUTH-002",
                    "type": "functional",
                    "priority": "HIGH",
                    "statement": "IF login attempts exceed 5 within 15 minutes THEN the system SHALL lock the account for 30 minutes",
                    "acceptance_criteria": [
                        "Counter increments on failed attempts",
                        "Lock activates after 5th attempt",
                        "Account unlocks after 30 minutes"
                    ]
                },
                {
                    "id": "REQ-AUTH-003",
                    "type": "non-functional",
                    "priority": "MEDIUM",
                    "statement": "The authentication service SHALL respond within 2 seconds for 95% of requests",
                    "acceptance_criteria": [
                        "P95 latency < 2000ms",
                        "Measured over 24-hour period"
                    ]
                },
                {
                    "id": "REQ-AUTH-004",
                    "type": "security",
                    "priority": "HIGH",
                    "statement": "The system SHALL store passwords using bcrypt with a minimum work factor of 12",
                    "acceptance_criteria": [
                        "Passwords hashed with bcrypt",
                        "Work factor >= 12",
                        "Salt generated for each password"
                    ]
                }
            ],
            "traceability_matrix": {
                "REQ-AUTH-001": ["DESIGN-001", "TEST-001", "TEST-002"],
                "REQ-AUTH-002": ["DESIGN-002", "TEST-003"],
                "REQ-AUTH-003": ["DESIGN-003", "TEST-004"],
                "REQ-AUTH-004": ["DESIGN-004", "TEST-005"]
            },
            "statistics": {
                "total_requirements": 4,
                "functional": 2,
                "non_functional": 1,
                "security": 1,
                "high_priority": 3
            }
        }


class DesignSpecWriterAgent(BaseAgent):
    """Technical design document generation"""
    
    def __init__(self):
        super().__init__(
            "design-spec-writer",
            ["architecture_design", "component_modeling", "interface_definition", "data_modeling"]
        )
    
    async def execute(self, task: str, context: Dict) -> Dict:
        print(f"\n🏗️ Design Spec Writer Agent: {task}")
        await asyncio.sleep(0.5)
        
        requirements = context.get("requirements", {})
        architecture = context.get("architecture", "microservices")
        
        return {
            "status": "success",
            "document": "design_spec_authentication_v1.0.md",
            "architecture": {
                "style": architecture,
                "components": [
                    {
                        "name": "AuthService",
                        "type": "microservice",
                        "responsibilities": ["User authentication", "Token generation", "Session management"],
                        "technologies": ["Python", "FastAPI", "PostgreSQL", "Redis"]
                    },
                    {
                        "name": "API Gateway",
                        "type": "infrastructure",
                        "responsibilities": ["Request routing", "Rate limiting", "Token validation"],
                        "technologies": ["Kong", "Nginx"]
                    },
                    {
                        "name": "UserDatabase",
                        "type": "database",
                        "responsibilities": ["User data persistence", "Credential storage"],
                        "technologies": ["PostgreSQL", "bcrypt"]
                    }
                ]
            },
            "interfaces": [
                {
                    "name": "POST /auth/login",
                    "input": {"username": "string", "password": "string"},
                    "output": {"token": "string", "expires_in": "integer"},
                    "errors": ["401 Unauthorized", "429 Too Many Requests"]
                },
                {
                    "name": "POST /auth/logout",
                    "input": {"token": "string"},
                    "output": {"success": "boolean"},
                    "errors": ["401 Unauthorized"]
                }
            ],
            "data_models": [
                {
                    "name": "User",
                    "fields": [
                        {"name": "id", "type": "UUID", "required": True},
                        {"name": "username", "type": "string", "required": True},
                        {"name": "password_hash", "type": "string", "required": True},
                        {"name": "created_at", "type": "timestamp", "required": True}
                    ]
                }
            ],
            "design_patterns": ["Repository Pattern", "Factory Pattern", "Circuit Breaker"],
            "security_considerations": [
                "All passwords hashed with bcrypt",
                "JWTs signed with RS256",
                "Rate limiting on login endpoint",
                "Account lockout after failed attempts"
            ]
        }


class SpecTasksWriterAgent(BaseAgent):
    """Implementation task breakdown and planning"""
    
    def __init__(self):
        super().__init__(
            "spec-tasks-writer",
            ["task_breakdown", "effort_estimation", "dependency_mapping", "sprint_planning"]
        )
    
    async def execute(self, task: str, context: Dict) -> Dict:
        print(f"\n📊 Spec Tasks Writer Agent: {task}")
        await asyncio.sleep(0.5)
        
        design = context.get("design", {})
        team_size = context.get("team_size", 3)
        
        return {
            "status": "success",
            "document": "implementation_tasks_v1.0.json",
            "tasks": [
                {
                    "id": "TASK-001",
                    "title": "Set up project structure and dependencies",
                    "description": "Initialize Python project with FastAPI, configure Docker",
                    "effort_hours": 4,
                    "dependencies": [],
                    "assigned_to": None,
                    "status": "pending"
                },
                {
                    "id": "TASK-002",
                    "title": "Create database schema and models",
                    "description": "Design and implement User table, set up migrations",
                    "effort_hours": 6,
                    "dependencies": ["TASK-001"],
                    "assigned_to": None,
                    "status": "pending"
                },
                {
                    "id": "TASK-003",
                    "title": "Implement password hashing service",
                    "description": "Create bcrypt service for password hashing and verification",
                    "effort_hours": 3,
                    "dependencies": ["TASK-001"],
                    "assigned_to": None,
                    "status": "pending"
                },
                {
                    "id": "TASK-004",
                    "title": "Implement JWT token service",
                    "description": "Create service for JWT generation and validation",
                    "effort_hours": 4,
                    "dependencies": ["TASK-001"],
                    "assigned_to": None,
                    "status": "pending"
                },
                {
                    "id": "TASK-005",
                    "title": "Create login endpoint",
                    "description": "Implement POST /auth/login with validation and error handling",
                    "effort_hours": 8,
                    "dependencies": ["TASK-002", "TASK-003", "TASK-004"],
                    "assigned_to": None,
                    "status": "pending"
                },
                {
                    "id": "TASK-006",
                    "title": "Implement rate limiting",
                    "description": "Add rate limiting to login endpoint using Redis",
                    "effort_hours": 5,
                    "dependencies": ["TASK-005"],
                    "assigned_to": None,
                    "status": "pending"
                },
                {
                    "id": "TASK-007",
                    "title": "Write unit tests",
                    "description": "Create comprehensive unit tests for all services",
                    "effort_hours": 8,
                    "dependencies": ["TASK-005"],
                    "assigned_to": None,
                    "status": "pending"
                }
            ],
            "summary": {
                "total_tasks": 7,
                "total_effort_hours": 38,
                "estimated_duration_days": 38 / (team_size * 6),  # 6 hours per day per developer
                "critical_path": ["TASK-001", "TASK-002", "TASK-005", "TASK-006"]
            },
            "sprint_plan": {
                "sprint_1": ["TASK-001", "TASK-002", "TASK-003", "TASK-004"],
                "sprint_2": ["TASK-005", "TASK-006", "TASK-007"]
            }
        }


class SpecImplementerAgent(BaseAgent):
    """Code implementation from task specifications"""
    
    def __init__(self):
        super().__init__(
            "spec-implementer",
            ["code_generation", "task_execution", "progress_tracking", "integration"]
        )
    
    async def execute(self, task: str, context: Dict) -> Dict:
        print(f"\n💻 Spec Implementer Agent: {task}")
        await asyncio.sleep(0.5)
        
        task_id = context.get("task_id", "TASK-001")
        task_details = context.get("task_details", {})
        
        return {
            "status": "success",
            "task_id": task_id,
            "implementation": {
                "files_created": [
                    "src/auth/password_service.py",
                    "src/auth/jwt_service.py",
                    "tests/test_password_service.py"
                ],
                "files_modified": [
                    "src/main.py",
                    "requirements.txt"
                ],
                "lines_of_code": 245,
                "test_coverage": 92
            },
            "code_sample": '''
# src/auth/password_service.py
import bcrypt

class PasswordService:
    def __init__(self, work_factor: int = 12):
        self.work_factor = work_factor
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt(rounds=self.work_factor)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hash: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))
            ''',
            "tests_passed": True,
            "integration_status": "ready",
            "completion_percentage": 100
        }


class TestSpecWriterAgent(BaseAgent):
    """Test specification and test code generation"""
    
    def __init__(self):
        super().__init__(
            "test-spec-writer",
            ["test_generation", "coverage_analysis", "acceptance_testing", "test_documentation"]
        )
    
    async def execute(self, task: str, context: Dict) -> Dict:
        print(f"\n🧪 Test Spec Writer Agent: {task}")
        await asyncio.sleep(0.5)
        
        requirements = context.get("requirements", {})
        
        return {
            "status": "success",
            "document": "test_spec_authentication_v1.0.md",
            "test_suite": {
                "total_tests": 25,
                "unit_tests": 15,
                "integration_tests": 7,
                "e2e_tests": 3
            },
            "test_cases": [
                {
                    "id": "TEST-001",
                    "requirement": "REQ-AUTH-001",
                    "type": "unit",
                    "description": "Test successful login with valid credentials",
                    "steps": [
                        "Create user with known credentials",
                        "Call login with correct username/password",
                        "Verify 200 status code",
                        "Verify JWT token is returned"
                    ],
                    "expected_result": "User authenticated, JWT token generated"
                },
                {
                    "id": "TEST-002",
                    "requirement": "REQ-AUTH-001",
                    "type": "unit",
                    "description": "Test login failure with invalid credentials",
                    "steps": [
                        "Attempt login with wrong password",
                        "Verify 401 status code",
                        "Verify no token is returned"
                    ],
                    "expected_result": "Authentication fails, 401 returned"
                },
                {
                    "id": "TEST-003",
                    "requirement": "REQ-AUTH-002",
                    "type": "integration",
                    "description": "Test account lockout after failed attempts",
                    "steps": [
                        "Attempt login 5 times with wrong password",
                        "Verify account is locked",
                        "Wait 30 minutes",
                        "Verify account is unlocked"
                    ],
                    "expected_result": "Account locks and unlocks as specified"
                }
            ],
            "test_code_sample": '''
import pytest
from auth.services import AuthService

class TestAuthentication:
    @pytest.fixture
    def auth_service(self):
        return AuthService()
    
    def test_successful_login(self, auth_service):
        # Arrange
        username = "testuser"
        password = "securepass123"
        auth_service.create_user(username, password)
        
        # Act
        result = auth_service.login(username, password)
        
        # Assert
        assert result.status_code == 200
        assert result.token is not None
        assert len(result.token) > 0
            ''',
            "coverage_target": 90,
            "current_coverage": 0
        }


class SpecJudgeAgent(BaseAgent):
    """Spec document evaluation and quality assessment"""
    
    def __init__(self):
        super().__init__(
            "spec-judge",
            ["quality_assessment", "version_comparison", "best_selection", "improvement_suggestions"]
        )
    
    async def execute(self, task: str, context: Dict) -> Dict:
        print(f"\n⚖️ Spec Judge Agent: {task}")
        await asyncio.sleep(0.5)
        
        documents = context.get("documents", [])
        
        return {
            "status": "success",
            "evaluation": {
                "overall_score": 87,
                "breakdown": {
                    "requirements_quality": 92,
                    "design_quality": 85,
                    "task_clarity": 88,
                    "test_coverage": 83,
                    "documentation": 87
                }
            },
            "strengths": [
                "Clear EARS syntax in requirements",
                "Comprehensive error handling design",
                "Good test coverage planning",
                "Well-defined acceptance criteria"
            ],
            "weaknesses": [
                "Missing performance benchmarks",
                "Limited edge case coverage",
                "Could use more detailed data flow diagrams"
            ],
            "recommendations": [
                {
                    "area": "requirements",
                    "suggestion": "Add more non-functional requirements for scalability"
                },
                {
                    "area": "design",
                    "suggestion": "Include sequence diagrams for complex flows"
                },
                {
                    "area": "testing",
                    "suggestion": "Add chaos engineering test scenarios"
                }
            ],
            "version_comparison": {
                "best_version": "v1.2",
                "reason": "Most comprehensive coverage with clear traceability"
            }
        }


# Example Usage Functions
async def example_security_workflow():
    """Example: Complete security review workflow"""
    print("\n" + "="*60)
    print("SECURITY REVIEW WORKFLOW EXAMPLE")
    print("="*60)
    
    manager = AgentManager()
    
    # Step 1: Code review
    code_review = await manager.execute(
        "security-reviewer",
        "Review code for security vulnerabilities",
        {"repository": "main-api", "branch": "develop"}
    )
    
    # Step 2: Dependency scan
    dep_scan = await manager.execute(
        "security-reviewer",
        "Scan dependencies for vulnerabilities",
        {"package_file": "requirements.txt"}
    )
    
    # Step 3: Secret detection
    secret_scan = await manager.execute(
        "security-reviewer",
        "Detect hardcoded secrets",
        {"scan_path": "./", "exclude": [".git", "node_modules"]}
    )
    
    print("\n📊 Security Review Summary:")
    print(f"  Code vulnerabilities: {code_review['summary']['vulnerabilities_found']}")
    print(f"  Vulnerable dependencies: {dep_scan['vulnerable_count']}")
    print(f"  Secrets found: {secret_scan['secrets_count']}")
    
    return {
        "code_review": code_review,
        "dependency_scan": dep_scan,
        "secret_scan": secret_scan
    }


async def example_spec_development_workflow():
    """Example: Complete spec-driven development workflow"""
    print("\n" + "="*60)
    print("SPEC-DRIVEN DEVELOPMENT WORKFLOW EXAMPLE")
    print("="*60)
    
    manager = AgentManager()
    feature = "Payment Processing System"
    
    # Initialize workflow
    print(f"\n📁 Building: {feature}")
    
    # Load system prompts
    prompt_result = await manager.execute(
        "spec-system-prompt-loader",
        f"Initialize spec workflow for {feature}",
        {"workflow_type": "feature_development"}
    )
    
    # Generate requirements
    req_result = await manager.execute(
        "spec-requirements-writer",
        f"Generate requirements for {feature}",
        {"feature": feature, "components": ["payment gateway", "refunds", "webhooks"]}
    )
    
    # Create design
    design_result = await manager.execute(
        "design-spec-writer",
        "Create technical design",
        {"requirements": req_result["requirements"], "architecture": "event-driven"}
    )
    
    # Generate tasks
    tasks_result = await manager.execute(
        "spec-tasks-writer",
        "Break down into implementation tasks",
        {"design": design_result, "team_size": 4}
    )
    
    # Implement first task
    impl_result = await manager.execute(
        "spec-implementer",
        "Implement TASK-001",
        {"task_id": "TASK-001", "task_details": tasks_result["tasks"][0]}
    )
    
    # Generate tests
    test_result = await manager.execute(
        "test-spec-writer",
        "Generate test specifications",
        {"requirements": req_result["requirements"]}
    )
    
    # Evaluate quality
    eval_result = await manager.execute(
        "spec-judge",
        "Evaluate spec quality",
        {
            "documents": [
                req_result["document"],
                design_result["document"],
                test_result["document"]
            ]
        }
    )
    
    print(f"\n✅ Workflow completed")
    print(f"  Requirements: {len(req_result['requirements'])} generated")
    print(f"  Tasks: {len(tasks_result['tasks'])} created")
    print(f"  Quality Score: {eval_result['evaluation']['overall_score']}/100")
    
    return {
        "feature": feature,
        "requirements": req_result,
        "design": design_result,
        "tasks": tasks_result,
        "implementation": impl_result,
        "tests": test_result,
        "evaluation": eval_result
    }


async def example_deployment_preparation():
    """Example: Prepare for production deployment"""
    print("\n" + "="*60)
    print("DEPLOYMENT PREPARATION WORKFLOW EXAMPLE")
    print("="*60)
    
    manager = AgentManager()
    
    # Performance testing
    perf_result = await manager.execute(
        "performance-tester",
        "Run load tests for production readiness",
        {"users": 1000, "duration": "10m", "endpoints": ["/api/v1/*"]}
    )
    
    # Compliance check
    compliance_result = await manager.execute(
        "compliance-checker",
        "Verify compliance for production",
        {"standards": ["SOC2", "GDPR", "ISO27001"]}
    )
    
    # Security review
    security_result = await manager.execute(
        "security-reviewer",
        "Final security review before deployment",
        {"scope": "full", "severity_threshold": "medium"}
    )
    
    # Initialize deployment repository
    repo_result = await manager.execute(
        "repository-initializer",
        "Prepare deployment repository",
        {
            "repo_name": "production-release-v2.0",
            "template": "production-template",
            "environment": "production"
        }
    )
    
    print("\n📊 Deployment Readiness:")
    print(f"  Performance Score: {perf_result['results']['success_rate']}%")
    print(f"  Compliance Score: {compliance_result['overall_compliance']}%")
    print(f"  Security Issues: {security_result['summary']['vulnerabilities_found']}")
    print(f"  Repository: {repo_result['repository']['url']}")
    
    deployment_ready = (
        perf_result['results']['success_rate'] > 99 and
        compliance_result['overall_compliance'] > 90 and
        security_result['summary']['high_severity'] == 0
    )
    
    print(f"\n{'✅' if deployment_ready else '❌'} Deployment {'APPROVED' if deployment_ready else 'BLOCKED'}")
    
    return {
        "performance": perf_result,
        "compliance": compliance_result,
        "security": security_result,
        "repository": repo_result,
        "deployment_ready": deployment_ready
    }


async def main():
    """Main function to run all agent examples"""
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "CLAUDE AGENT EXAMPLES" + " "*22 + "║")
    print("║" + " "*10 + "Demonstrating All 11 Plugin Agents" + " "*13 + "║")
    print("╚" + "="*58 + "╝")
    
    # Run example workflows
    security_results = await example_security_workflow()
    spec_results = await example_spec_development_workflow()
    deployment_results = await example_deployment_preparation()
    
    # Summary
    print("\n" + "="*60)
    print("EXECUTION SUMMARY")
    print("="*60)
    print("✅ All agent demonstrations completed successfully")
    print("\nAgents demonstrated:")
    print("  • Security Reviewer")
    print("  • Performance Tester")
    print("  • Compliance Checker")
    print("  • Repository Initializer")
    print("  • Spec System Prompt Loader")
    print("  • Spec Requirements Writer")
    print("  • Design Spec Writer")
    print("  • Spec Tasks Writer")
    print("  • Spec Implementer")
    print("  • Test Spec Writer")
    print("  • Spec Judge")
    
    return {
        "security_workflow": security_results,
        "spec_workflow": spec_results,
        "deployment_workflow": deployment_results
    }


if __name__ == "__main__":
    # Run the async main function
    results = asyncio.run(main())
    
    # Save results
    with open("agent_demo_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print("\n📁 Results saved to agent_demo_results.json")
