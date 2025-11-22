#!/usr/bin/env python3
"""
Claude DevOps Plugin - Skills Demonstration
Demonstrates code-reviewer and pdf-processor skills with practical examples
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import tempfile


@dataclass
class CodeFile:
    """Represents a code file for review"""
    path: str
    language: str
    content: str
    lines: int


@dataclass
class PDFDocument:
    """Represents a PDF document for processing"""
    path: str
    title: str
    pages: int
    size_kb: int


class SkillsManager:
    """Manager for plugin skills"""
    
    def __init__(self):
        self.available_skills = {
            "code-reviewer": CodeReviewerSkill(),
            "pdf-processor": PDFProcessorSkill()
        }
        self.execution_history = []
    
    async def apply_skill(self, skill_name: str, target: Any, options: Dict = None) -> Dict:
        """Apply a skill to a target"""
        if skill_name not in self.available_skills:
            return {"error": f"Unknown skill: {skill_name}"}
        
        skill = self.available_skills[skill_name]
        result = await skill.apply(target, options or {})
        
        # Log execution
        self.execution_history.append({
            "timestamp": datetime.now().isoformat(),
            "skill": skill_name,
            "target": str(target),
            "success": result.get("status") == "success"
        })
        
        return result


class CodeReviewerSkill:
    """Advanced code review skill"""
    
    def __init__(self):
        self.name = "code-reviewer"
        self.supported_languages = [
            "python", "javascript", "typescript", "java", "go", "rust", "c++", "ruby"
        ]
        self.review_categories = [
            "syntax", "style", "complexity", "security", "performance", 
            "best_practices", "documentation", "testing"
        ]
    
    async def apply(self, target: CodeFile, options: Dict) -> Dict:
        """Apply code review to a file or directory"""
        print(f"\n🔍 Code Reviewer Skill: Analyzing {target.path}")
        print(f"   Language: {target.language}")
        print(f"   Lines of code: {target.lines}")
        
        # Perform various analyses
        results = {
            "status": "success",
            "file": target.path,
            "language": target.language,
            "timestamp": datetime.now().isoformat(),
            "summary": {},
            "findings": [],
            "metrics": {},
            "suggestions": []
        }
        
        # Syntax analysis
        print("   ✓ Checking syntax...")
        await asyncio.sleep(0.3)
        syntax_issues = await self._check_syntax(target)
        results["findings"].extend(syntax_issues)
        
        # Style analysis
        print("   ✓ Analyzing code style...")
        await asyncio.sleep(0.3)
        style_issues = await self._check_style(target)
        results["findings"].extend(style_issues)
        
        # Complexity analysis
        print("   ✓ Measuring complexity...")
        await asyncio.sleep(0.3)
        complexity_metrics = await self._analyze_complexity(target)
        results["metrics"]["complexity"] = complexity_metrics
        
        # Security analysis
        print("   ✓ Security scanning...")
        await asyncio.sleep(0.3)
        security_issues = await self._check_security(target)
        results["findings"].extend(security_issues)
        
        # Performance analysis
        print("   ✓ Performance analysis...")
        await asyncio.sleep(0.3)
        performance_issues = await self._check_performance(target)
        results["findings"].extend(performance_issues)
        
        # Best practices
        print("   ✓ Checking best practices...")
        await asyncio.sleep(0.3)
        best_practices = await self._check_best_practices(target)
        results["suggestions"].extend(best_practices)
        
        # Calculate summary
        results["summary"] = self._calculate_summary(results["findings"])
        results["score"] = self._calculate_score(results)
        
        return results
    
    async def _check_syntax(self, file: CodeFile) -> List[Dict]:
        """Check for syntax issues"""
        issues = []
        
        if file.language == "python":
            # Simulate Python-specific checks
            issues.append({
                "type": "syntax",
                "severity": "error",
                "line": 45,
                "column": 12,
                "message": "Missing colon after if statement",
                "rule": "E901"
            })
        elif file.language == "javascript":
            # Simulate JavaScript-specific checks
            issues.append({
                "type": "syntax",
                "severity": "warning",
                "line": 23,
                "column": 8,
                "message": "Missing semicolon",
                "rule": "semi"
            })
        
        return issues
    
    async def _check_style(self, file: CodeFile) -> List[Dict]:
        """Check code style"""
        issues = [
            {
                "type": "style",
                "severity": "info",
                "line": 12,
                "message": "Line too long (exceeds 100 characters)",
                "rule": "max-line-length"
            },
            {
                "type": "style",
                "severity": "info",
                "line": 34,
                "message": "Inconsistent indentation",
                "rule": "indent"
            }
        ]
        return issues
    
    async def _analyze_complexity(self, file: CodeFile) -> Dict:
        """Analyze code complexity"""
        return {
            "cyclomatic": 12,
            "cognitive": 8,
            "halstead": {
                "difficulty": 15.3,
                "volume": 245.6,
                "effort": 3759.68
            },
            "maintainability_index": 72,
            "functions": {
                "total": 15,
                "complex": 3,
                "very_complex": 1
            }
        }
    
    async def _check_security(self, file: CodeFile) -> List[Dict]:
        """Check for security issues"""
        issues = []
        
        # Simulate security checks based on language
        if file.language in ["python", "javascript", "java"]:
            issues.append({
                "type": "security",
                "severity": "high",
                "line": 78,
                "message": "Potential SQL injection vulnerability",
                "cwe": "CWE-89",
                "owasp": "A03:2021"
            })
            
            issues.append({
                "type": "security",
                "severity": "medium",
                "line": 102,
                "message": "Hardcoded credential detected",
                "cwe": "CWE-798",
                "owasp": "A07:2021"
            })
        
        return issues
    
    async def _check_performance(self, file: CodeFile) -> List[Dict]:
        """Check for performance issues"""
        return [
            {
                "type": "performance",
                "severity": "warning",
                "line": 156,
                "message": "Inefficient loop - consider using list comprehension",
                "impact": "medium"
            },
            {
                "type": "performance",
                "severity": "info",
                "line": 234,
                "message": "Multiple database calls in loop - consider batch operation",
                "impact": "high"
            }
        ]
    
    async def _check_best_practices(self, file: CodeFile) -> List[str]:
        """Check best practices and generate suggestions"""
        suggestions = [
            "Add docstrings to all public functions",
            "Consider using type hints for better code clarity",
            "Implement error handling for external API calls",
            "Add unit tests for critical functions",
            "Consider extracting complex logic into separate functions"
        ]
        
        if file.language == "python":
            suggestions.append("Use context managers for file operations")
            suggestions.append("Consider using dataclasses for data structures")
        elif file.language in ["javascript", "typescript"]:
            suggestions.append("Use async/await instead of callbacks")
            suggestions.append("Consider using const for immutable values")
        
        return suggestions
    
    def _calculate_summary(self, findings: List[Dict]) -> Dict:
        """Calculate findings summary"""
        summary = {
            "total": len(findings),
            "by_severity": {},
            "by_type": {}
        }
        
        for finding in findings:
            # Count by severity
            severity = finding.get("severity", "info")
            summary["by_severity"][severity] = summary["by_severity"].get(severity, 0) + 1
            
            # Count by type
            finding_type = finding.get("type", "other")
            summary["by_type"][finding_type] = summary["by_type"].get(finding_type, 0) + 1
        
        return summary
    
    def _calculate_score(self, results: Dict) -> int:
        """Calculate overall code quality score"""
        score = 100
        
        # Deduct points for issues
        for finding in results["findings"]:
            if finding["severity"] == "error":
                score -= 10
            elif finding["severity"] == "high":
                score -= 7
            elif finding["severity"] == "warning":
                score -= 3
            elif finding["severity"] == "info":
                score -= 1
        
        # Adjust for complexity
        complexity = results["metrics"]["complexity"]["cyclomatic"]
        if complexity > 20:
            score -= 10
        elif complexity > 10:
            score -= 5
        
        return max(0, score)


class PDFProcessorSkill:
    """PDF processing and analysis skill"""
    
    def __init__(self):
        self.name = "pdf-processor"
        self.supported_operations = [
            "extract_text", "extract_metadata", "summarize", 
            "extract_tables", "extract_images", "merge", "split", "compress"
        ]
    
    async def apply(self, target: PDFDocument, options: Dict) -> Dict:
        """Process PDF document"""
        print(f"\n📄 PDF Processor Skill: Processing {target.path}")
        print(f"   Title: {target.title}")
        print(f"   Pages: {target.pages}")
        print(f"   Size: {target.size_kb}KB")
        
        operations = options.get("operations", ["extract_text", "extract_metadata", "summarize"])
        results = {
            "status": "success",
            "document": target.path,
            "timestamp": datetime.now().isoformat(),
            "operations_performed": []
        }
        
        for operation in operations:
            if operation in self.supported_operations:
                print(f"   ✓ Performing: {operation}...")
                await asyncio.sleep(0.3)
                
                if operation == "extract_text":
                    results["extracted_text"] = await self._extract_text(target)
                elif operation == "extract_metadata":
                    results["metadata"] = await self._extract_metadata(target)
                elif operation == "summarize":
                    results["summary"] = await self._summarize(target)
                elif operation == "extract_tables":
                    results["tables"] = await self._extract_tables(target)
                elif operation == "extract_images":
                    results["images"] = await self._extract_images(target)
                
                results["operations_performed"].append(operation)
        
        return results
    
    async def _extract_text(self, doc: PDFDocument) -> Dict:
        """Extract text from PDF"""
        # Simulate text extraction
        sample_text = f"""
        This is extracted text from {doc.title}.
        
        The document contains important information about DevOps practices,
        including CI/CD pipelines, monitoring strategies, and deployment procedures.
        
        Key sections include:
        1. Introduction to DevOps
        2. Setting up CI/CD pipelines
        3. Monitoring and alerting
        4. Security best practices
        5. Troubleshooting guide
        
        Total words extracted: {doc.pages * 250}
        """
        
        return {
            "full_text": sample_text,
            "word_count": doc.pages * 250,
            "character_count": len(sample_text),
            "pages_processed": doc.pages
        }
    
    async def _extract_metadata(self, doc: PDFDocument) -> Dict:
        """Extract metadata from PDF"""
        return {
            "title": doc.title,
            "author": "DevOps Team",
            "subject": "DevOps Documentation",
            "keywords": ["DevOps", "CI/CD", "Automation", "Monitoring"],
            "creator": "Claude DevOps Plugin",
            "producer": "PDF Processor Skill v1.0",
            "creation_date": "2024-11-15T10:30:00Z",
            "modification_date": "2024-11-20T14:45:00Z",
            "pages": doc.pages,
            "file_size": f"{doc.size_kb}KB",
            "pdf_version": "1.7",
            "encrypted": False
        }
    
    async def _summarize(self, doc: PDFDocument) -> Dict:
        """Generate document summary"""
        return {
            "executive_summary": f"""
            {doc.title} provides comprehensive guidance on DevOps practices and procedures.
            The document covers essential topics including continuous integration/deployment,
            infrastructure as code, monitoring solutions, and security considerations.
            """.strip(),
            "key_points": [
                "Automated CI/CD pipeline setup and configuration",
                "Container orchestration with Kubernetes",
                "Monitoring stack implementation (Prometheus, Grafana)",
                "Security scanning and compliance automation",
                "Incident response and troubleshooting procedures"
            ],
            "recommendations": [
                "Implement automated testing at all stages",
                "Use infrastructure as code for all deployments",
                "Establish comprehensive monitoring coverage",
                "Regular security audits and updates"
            ],
            "summary_length": "short",
            "confidence": 0.92
        }
    
    async def _extract_tables(self, doc: PDFDocument) -> List[Dict]:
        """Extract tables from PDF"""
        return [
            {
                "table_id": 1,
                "page": 5,
                "title": "Deployment Environments",
                "headers": ["Environment", "Purpose", "Access Level", "Approval Required"],
                "rows": [
                    ["Development", "Developer testing", "All developers", "No"],
                    ["Staging", "QA testing", "QA team", "QA Lead"],
                    ["Production", "Live system", "Ops team only", "CTO"]
                ]
            },
            {
                "table_id": 2,
                "page": 12,
                "title": "Monitoring Metrics",
                "headers": ["Metric", "Threshold", "Alert Level", "Action"],
                "rows": [
                    ["CPU Usage", ">80%", "Warning", "Scale up"],
                    ["Memory Usage", ">90%", "Critical", "Immediate intervention"],
                    ["Error Rate", ">1%", "Warning", "Investigation required"]
                ]
            }
        ]
    
    async def _extract_images(self, doc: PDFDocument) -> List[Dict]:
        """Extract images from PDF"""
        return [
            {
                "image_id": 1,
                "page": 3,
                "type": "diagram",
                "description": "CI/CD Pipeline Architecture",
                "format": "PNG",
                "dimensions": "800x600",
                "file_path": "/tmp/extracted_images/pipeline_diagram.png"
            },
            {
                "image_id": 2,
                "page": 8,
                "type": "chart",
                "description": "Performance Metrics Dashboard",
                "format": "JPEG",
                "dimensions": "1200x800",
                "file_path": "/tmp/extracted_images/metrics_dashboard.jpg"
            }
        ]


# Example usage functions
async def example_code_review_workflow():
    """Complete code review workflow"""
    print("\n" + "="*70)
    print("CODE REVIEW WORKFLOW EXAMPLE")
    print("="*70)
    
    manager = SkillsManager()
    
    # Create sample code files for review
    code_files = [
        CodeFile(
            path="src/api/auth_handler.py",
            language="python",
            content="# Authentication handler code",
            lines=245
        ),
        CodeFile(
            path="src/frontend/components/Dashboard.tsx",
            language="typescript",
            content="// Dashboard component",
            lines=189
        ),
        CodeFile(
            path="src/services/database.js",
            language="javascript",
            content="// Database service",
            lines=312
        )
    ]
    
    review_results = []
    
    for code_file in code_files:
        print(f"\n📝 Reviewing: {code_file.path}")
        
        result = await manager.apply_skill(
            "code-reviewer",
            code_file,
            {
                "checks": ["syntax", "style", "security", "performance"],
                "severity_threshold": "warning"
            }
        )
        
        review_results.append(result)
        
        # Print summary
        print(f"   Score: {result['score']}/100")
        print(f"   Issues: {result['summary']['total']}")
        if result["summary"]["by_severity"]:
            for severity, count in result["summary"]["by_severity"].items():
                print(f"     - {severity}: {count}")
    
    # Overall summary
    print("\n📊 Code Review Summary:")
    total_issues = sum(r["summary"]["total"] for r in review_results)
    avg_score = sum(r["score"] for r in review_results) / len(review_results)
    
    print(f"   Files reviewed: {len(code_files)}")
    print(f"   Total issues: {total_issues}")
    print(f"   Average score: {avg_score:.1f}/100")
    
    # Critical issues requiring attention
    critical_issues = []
    for result in review_results:
        for finding in result["findings"]:
            if finding.get("severity") in ["error", "high"]:
                critical_issues.append({
                    "file": result["file"],
                    "issue": finding
                })
    
    if critical_issues:
        print(f"\n⚠️ Critical Issues Requiring Immediate Attention:")
        for issue in critical_issues[:3]:  # Show top 3
            print(f"   - {issue['file']}: {issue['issue']['message']}")
    
    return {
        "files_reviewed": len(code_files),
        "results": review_results,
        "total_issues": total_issues,
        "average_score": avg_score,
        "critical_issues": critical_issues
    }


async def example_pdf_processing_workflow():
    """PDF document processing workflow"""
    print("\n" + "="*70)
    print("PDF PROCESSING WORKFLOW EXAMPLE")
    print("="*70)
    
    manager = SkillsManager()
    
    # Create sample PDF documents
    documents = [
        PDFDocument(
            path="docs/deployment_guide.pdf",
            title="Deployment Guide v2.0",
            pages=45,
            size_kb=1250
        ),
        PDFDocument(
            path="docs/security_policies.pdf",
            title="Security Policies and Procedures",
            pages=78,
            size_kb=2340
        ),
        PDFDocument(
            path="reports/monthly_metrics.pdf",
            title="Monthly Performance Metrics",
            pages=12,
            size_kb=456
        )
    ]
    
    processed_docs = []
    
    for doc in documents:
        print(f"\n📄 Processing: {doc.title}")
        
        # Different operations for different document types
        if "guide" in doc.title.lower():
            operations = ["extract_text", "extract_metadata", "summarize", "extract_tables"]
        elif "security" in doc.title.lower():
            operations = ["extract_text", "summarize", "extract_tables"]
        else:
            operations = ["extract_metadata", "summarize", "extract_tables", "extract_images"]
        
        result = await manager.apply_skill(
            "pdf-processor",
            doc,
            {"operations": operations}
        )
        
        processed_docs.append(result)
        
        # Print operation results
        print(f"   Operations completed: {len(result['operations_performed'])}")
        for op in result["operations_performed"]:
            print(f"     ✓ {op}")
    
    # Generate consolidated report
    print("\n📊 PDF Processing Summary:")
    print(f"   Documents processed: {len(documents)}")
    
    total_pages = sum(doc.pages for doc in documents)
    total_size = sum(doc.size_kb for doc in documents)
    
    print(f"   Total pages: {total_pages}")
    print(f"   Total size: {total_size/1024:.1f}MB")
    
    # Extract key information
    print("\n📌 Key Information Extracted:")
    for i, result in enumerate(processed_docs):
        if "summary" in result:
            print(f"\n   {documents[i].title}:")
            for point in result["summary"]["key_points"][:2]:
                print(f"     • {point}")
    
    return {
        "documents_processed": len(documents),
        "total_pages": total_pages,
        "results": processed_docs
    }


async def example_combined_skills_workflow():
    """Workflow combining multiple skills"""
    print("\n" + "="*70)
    print("COMBINED SKILLS WORKFLOW: Documentation Review")
    print("="*70)
    
    manager = SkillsManager()
    
    # Step 1: Extract code samples from PDF documentation
    print("\n📍 Step 1: Extract code samples from documentation")
    
    doc = PDFDocument(
        path="docs/api_documentation.pdf",
        title="API Documentation",
        pages=35,
        size_kb=890
    )
    
    pdf_result = await manager.apply_skill(
        "pdf-processor",
        doc,
        {"operations": ["extract_text", "extract_tables"]}
    )
    
    print("   ✓ Code samples extracted from documentation")
    
    # Step 2: Review extracted code samples
    print("\n📍 Step 2: Review code quality in documentation")
    
    # Simulate extracted code samples
    code_samples = [
        CodeFile(
            path="docs/samples/auth_example.py",
            language="python",
            content="""
def authenticate(username, password):
    # Sample authentication code from docs
    query = f"SELECT * FROM users WHERE username='{username}'"
    # ... rest of code
            """,
            lines=25
        ),
        CodeFile(
            path="docs/samples/api_client.js",
            language="javascript",
            content="""
// API client example
fetch('/api/data')
    .then(response => response.json())
    .then(data => console.log(data))
            """,
            lines=15
        )
    ]
    
    review_results = []
    for sample in code_samples:
        result = await manager.apply_skill(
            "code-reviewer",
            sample,
            {"checks": ["security", "best_practices"]}
        )
        review_results.append(result)
        
        print(f"   ✓ Reviewed: {sample.path} (Score: {result['score']}/100)")
    
    # Step 3: Generate updated documentation
    print("\n📍 Step 3: Generate recommendations for documentation update")
    
    recommendations = []
    for i, review in enumerate(review_results):
        if review["score"] < 70:
            recommendations.append({
                "sample": code_samples[i].path,
                "issues": review["summary"]["total"],
                "priority": "high" if review["score"] < 50 else "medium",
                "suggestions": review["suggestions"][:2]
            })
    
    print(f"   ✓ Generated {len(recommendations)} recommendations")
    
    # Step 4: Create summary report
    print("\n📊 Documentation Review Summary:")
    print(f"   Documentation pages: {doc.pages}")
    print(f"   Code samples reviewed: {len(code_samples)}")
    print(f"   Average code quality score: {sum(r['score'] for r in review_results) / len(review_results):.1f}/100")
    print(f"   Recommendations: {len(recommendations)}")
    
    if recommendations:
        print("\n   Priority Updates Required:")
        for rec in recommendations:
            print(f"     • {rec['sample']}: {rec['issues']} issues ({rec['priority']} priority)")
    
    return {
        "documentation": doc.title,
        "code_samples_reviewed": len(code_samples),
        "review_results": review_results,
        "recommendations": recommendations
    }


async def example_automated_report_generation():
    """Generate automated reports using skills"""
    print("\n" + "="*70)
    print("AUTOMATED REPORT GENERATION")
    print("="*70)
    
    manager = SkillsManager()
    
    print("\n📝 Generating Weekly DevOps Report...")
    
    # 1. Code quality assessment
    print("\n   Section 1: Code Quality")
    code_files = [
        CodeFile("src/main.py", "python", "", 450),
        CodeFile("src/api.js", "javascript", "", 320),
        CodeFile("src/database.go", "go", "", 280)
    ]
    
    code_reviews = []
    for file in code_files:
        result = await manager.apply_skill("code-reviewer", file, {})
        code_reviews.append({
            "file": file.path,
            "score": result["score"],
            "issues": result["summary"]["total"]
        })
    
    # 2. Documentation review
    print("\n   Section 2: Documentation Status")
    docs = [
        PDFDocument("docs/user_guide.pdf", "User Guide", 25, 650),
        PDFDocument("docs/api_reference.pdf", "API Reference", 40, 980)
    ]
    
    doc_summaries = []
    for doc in docs:
        result = await manager.apply_skill(
            "pdf-processor",
            doc,
            {"operations": ["extract_metadata", "summarize"]}
        )
        doc_summaries.append({
            "document": doc.title,
            "pages": doc.pages,
            "last_modified": result["metadata"]["modification_date"]
        })
    
    # 3. Generate report
    print("\n   Section 3: Compiling Report")
    await asyncio.sleep(0.5)
    
    report = {
        "title": "Weekly DevOps Report",
        "generated_at": datetime.now().isoformat(),
        "sections": {
            "code_quality": {
                "files_reviewed": len(code_files),
                "average_score": sum(r["score"] for r in code_reviews) / len(code_reviews),
                "total_issues": sum(r["issues"] for r in code_reviews),
                "details": code_reviews
            },
            "documentation": {
                "documents_reviewed": len(docs),
                "total_pages": sum(d.pages for d in docs),
                "details": doc_summaries
            },
            "recommendations": [
                "Address high-priority security issues in code",
                "Update API documentation with latest changes",
                "Improve code coverage in critical modules",
                "Schedule documentation review meeting"
            ]
        }
    }
    
    print("\n✅ Report Generated Successfully")
    print(f"   Title: {report['title']}")
    print(f"   Code Quality Score: {report['sections']['code_quality']['average_score']:.1f}/100")
    print(f"   Documentation Pages: {report['sections']['documentation']['total_pages']}")
    
    return report


async def main():
    """Main function to run all skill examples"""
    print("╔" + "="*68 + "╗")
    print("║" + " "*20 + "CLAUDE SKILLS DEMONSTRATION" + " "*20 + "║")
    print("║" + " "*10 + "Code Reviewer and PDF Processor Skills" + " "*19 + "║")
    print("╚" + "="*68 + "╝")
    
    # Run examples
    code_review = await example_code_review_workflow()
    pdf_processing = await example_pdf_processing_workflow()
    combined = await example_combined_skills_workflow()
    report = await example_automated_report_generation()
    
    # Summary
    print("\n" + "="*70)
    print("EXECUTION SUMMARY")
    print("="*70)
    print("✅ All skill demonstrations completed successfully")
    
    print("\nSkills demonstrated:")
    print("  • code-reviewer - Advanced code analysis and review")
    print("  • pdf-processor - PDF document processing and extraction")
    
    print("\nCapabilities shown:")
    print("  • Syntax and style checking")
    print("  • Security vulnerability detection")
    print("  • Performance analysis")
    print("  • Complexity measurement")
    print("  • PDF text and metadata extraction")
    print("  • Document summarization")
    print("  • Table and image extraction")
    
    print("\nWorkflows covered:")
    print("  • Complete code review process")
    print("  • PDF document processing")
    print("  • Combined skills workflow")
    print("  • Automated report generation")
    
    # Save results
    results = {
        "code_review_workflow": code_review,
        "pdf_processing_workflow": pdf_processing,
        "combined_workflow": combined,
        "automated_report": report
    }
    
    with open("skills_demo_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print("\n📁 Results saved to skills_demo_results.json")
    
    return results


if __name__ == "__main__":
    asyncio.run(main())
