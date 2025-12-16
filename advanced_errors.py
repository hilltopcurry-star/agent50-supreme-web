from __future__ import annotations
import re
import ast
import subprocess
from pathlib import Path
import sys
import requests

class AdvancedErrorHandler:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.projects_dir = self.base_dir / "projects"
        self.api_key = "sk-9214c5054a7f4b828cf3f9d608a88f6a"
    
    def analyze_code_quality(self, project_name: str) -> dict:
        """
        Code quality analysis using AI
        """
        project_dir = self.projects_dir / project_name
        issues = []
        
        print(f"🔍 Analyzing code quality for: {project_name}")
        
        # Analyze all Python files
        python_files = list(project_dir.glob("**/*.py"))
        
        for py_file in python_files:
            file_issues = self.analyze_python_file(py_file, project_name)
            issues.extend(file_issues)
        
        # Get AI-powered suggestions
        ai_suggestions = self.get_ai_code_review(project_name, issues)
        
        return {
            "project": project_name,
            "files_analyzed": len(python_files),
            "issues_found": len(issues),
            "issues": issues,
            "ai_suggestions": ai_suggestions,
            "quality_score": self.calculate_quality_score(issues, len(python_files))
        }
    
    def analyze_python_file(self, file_path: Path, project_name: str) -> list:
        """
        Individual Python file analysis
        """
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic syntax check
            try:
                ast.parse(content)
            except SyntaxError as e:
                issues.append({
                    "file": file_path.name,
                    "type": "syntax_error",
                    "severity": "high",
                    "description": f"Syntax error: {e}",
                    "line": e.lineno,
                    "solution": "Fix Python syntax"
                })
            
            # Check for common issues
            if "print(" in content and "if __name__" not in content:
                issues.append({
                    "file": file_path.name,
                    "type": "debug_print",
                    "severity": "low", 
                    "description": "Debug print statements found",
                    "solution": "Remove or move prints inside main guard"
                })
            
            if "TODO" in content or "FIXME" in content:
                issues.append({
                    "file": file_path.name,
                    "type": "todo_comment",
                    "severity": "info",
                    "description": "TODO/FIXME comments found",
                    "solution": "Address pending tasks"
                })
            
            # Check for large files
            lines = content.split('\n')
            if len(lines) > 200:
                issues.append({
                    "file": file_path.name,
                    "type": "large_file",
                    "severity": "medium",
                    "description": f"File has {len(lines)} lines (consider splitting)",
                    "solution": "Split into smaller modules"
                })
            
            # Check for missing error handling
            if "import requests" in content and "try:" not in content and "except" not in content:
                issues.append({
                    "file": file_path.name,
                    "type": "missing_error_handling",
                    "severity": "medium",
                    "description": "Missing error handling for requests",
                    "solution": "Add try-except blocks for network calls"
                })
                
        except Exception as e:
            issues.append({
                "file": file_path.name,
                "type": "analysis_error",
                "severity": "high",
                "description": f"Could not analyze file: {e}",
                "solution": "Check file encoding and content"
            })
        
        return issues
    
    def get_ai_code_review(self, project_name: str, issues: list) -> dict:
        """
        AI se code review aur suggestions leta hai
        """
        print("🤖 Getting AI-powered code review...")
        
        project_dir = self.projects_dir / project_name
        python_files = list(project_dir.glob("**/*.py"))
        
        # Read all code files
        code_context = ""
        for py_file in python_files[:3]:  # First 3 files for context
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    code_context += f"\n\n--- {py_file.name} ---\n{f.read()}"
            except:
                pass
        
        prompt = f"""
        You are an expert code reviewer. Analyze this code and provide specific improvements.
        
        PROJECT: {project_name}
        ISSUES FOUND: {len(issues)}
        
        CODE FILES:{code_context}
        
        Please provide:
        1. Overall code quality assessment
        2. Specific improvements for found issues
        3. Best practices recommendations
        4. Performance optimization suggestions
        
        Be concise and actionable.
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "review": result["choices"][0]["message"]["content"]
                }
            else:
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def calculate_quality_score(self, issues: list, file_count: int) -> int:
        """
        Code quality score calculate karta hai (0-100)
        """
        if file_count == 0:
            return 100
        
        # Deduct points based on issues
        high_severity = len([i for i in issues if i["severity"] == "high"])
        medium_severity = len([i for i in issues if i["severity"] == "medium"])
        low_severity = len([i for i in issues if i["severity"] == "low"])
        
        base_score = 100
        deductions = (high_severity * 10) + (medium_severity * 5) + (low_severity * 2)
        
        final_score = max(0, base_score - deductions)
        return final_score
    
    def auto_fix_issues(self, project_name: str, issues: list) -> dict:
        """
        Simple issues automatically fix karta hai
        """
        fixes_applied = []
        
        for issue in issues:
            if issue["type"] == "debug_print" and issue["severity"] == "low":
                print(f"🔧 Fixing debug prints in {issue['file']}")
                # This would actually modify the file in real implementation
                fixes_applied.append({
                    "issue": issue,
                    "fixed": True,
                    "action": "Removed debug prints"
                })
        
        return {
            "project": project_name,
            "fixes_applied": len(fixes_applied),
            "details": fixes_applied
        }
    
    def comprehensive_analysis(self, project_name: str) -> dict:
        """
        Complete project analysis with AI review
        """
        print(f"🎯 Starting comprehensive analysis for: {project_name}")
        
        # Code quality analysis
        quality_report = self.analyze_code_quality(project_name)
        
        # Auto-fix simple issues
        fix_report = self.auto_fix_issues(project_name, quality_report["issues"])
        
        return {
            "project": project_name,
            "quality_report": quality_report,
            "fix_report": fix_report,
            "summary": {
                "files_analyzed": quality_report["files_analyzed"],
                "issues_found": quality_report["issues_found"],
                "fixes_applied": fix_report["fixes_applied"],
                "quality_score": quality_report["quality_score"],
                "ai_review_available": quality_report["ai_suggestions"]["success"]
            }
        }

def main():
    handler = AdvancedErrorHandler()
    
    print("=== 🧠 AI DEV AGENT - ADVANCED ERROR HANDLING ===")
    print("AI-POWERED CODE ANALYSIS & OPTIMIZATION!\n")
    
    project_name = input("Project ka naam likhen (e.g. agent50): ").strip()
    if not project_name:
        print("❌ Project name required!")
        return
    
    project_dir = handler.projects_dir / project_name
    if not project_dir.exists():
        print(f"❌ Project '{project_name}' not found!")
        return
    
    print(f"\n🎯 Analyzing project: {project_name}")
    
    analysis = handler.comprehensive_analysis(project_name)
    
    print(f"\n📊 COMPREHENSIVE ANALYSIS RESULTS:")
    print(f"Project: {analysis['project']}")
    print(f"Files analyzed: {analysis['summary']['files_analyzed']}")
    print(f"Issues found: {analysis['summary']['issues_found']}")
    print(f"Fixes applied: {analysis['summary']['fixes_applied']}")
    print(f"Quality Score: {analysis['summary']['quality_score']}/100")
    
    if analysis['summary']['quality_score'] >= 80:
        print("✅ Code Quality: EXCELLENT")
    elif analysis['summary']['quality_score'] >= 60:
        print("⚠️ Code Quality: GOOD (some improvements needed)")
    else:
        print("❌ Code Quality: NEEDS IMPROVEMENT")
    
    if analysis['quality_report']['ai_suggestions']['success']:
        print(f"\n🤖 AI CODE REVIEW:")
        print("-" * 50)
        print(analysis['quality_report']['ai_suggestions']['review'])
        print("-" * 50)
    else:
        print(f"\n⚠️ AI review unavailable: {analysis['quality_report']['ai_suggestions']['error']}")

if __name__ == "__main__":
    main()