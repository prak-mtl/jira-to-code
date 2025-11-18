import os
from pathlib import Path
from typing import Dict, Any
import json
from datetime import datetime

class ContextBootstrap:
    """
    Bootstraps the .ai/ directory structure with context files
    for a new project using the Persona-Driven AI Framework.
    """
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.ai_dir = self.project_root / ".ai"
        self.rules_dir = self.ai_dir / "rules"
        self.workflow_dir = self.ai_dir / "workflow"
        
    def bootstrap(self, project_info: Dict[str, Any]) -> None:
        """
        Create complete .ai/ directory structure with context files
        
        Args:
            project_info: {
                "name": "project-name",
                "description": "project description",
                "tech_stack": ["Python", "FastAPI", "React"],
                "architecture_type": "microservices|monolith|serverless"
            }
        """
        print("🚀 Bootstrapping Persona-Driven AI Framework context...")
        
        # Create directory structure
        self._create_directories()
        
        # Generate context files
        self._generate_architecture_md(project_info)
        self._generate_coding_standards_md(project_info)
        self._generate_system_overview_md(project_info)
        self._generate_global_coverage_json(project_info)
        
        print("✅ Context bootstrap complete!")
        print(f"📁 Created: {self.ai_dir}")
        
    def _create_directories(self):
        """Create .ai/ directory structure"""
        dirs = [
            self.ai_dir,
            self.rules_dir,
            self.rules_dir / "feature",
            self.rules_dir / "packages",
            self.workflow_dir,
        ]
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            
    def _generate_architecture_md(self, project_info: Dict[str, Any]):
        """Generate ARCHITECTURE.md context file"""
        content = f"""# {project_info['name']} - Architecture

## System Overview

{project_info['description']}

## Technology Stack

{self._format_tech_stack(project_info.get('tech_stack', []))}

## Architecture Type

**Type**: {project_info.get('architecture_type', 'Not specified')}

## Project Structure

```
{project_info['name']}/
├── backend/          # Backend services
├── frontend/         # Frontend application
├── .ai/             # AI Context & Documentation
│   ├── rules/       # Architecture and coding standards
│   └── workflow/    # Generated workflow artifacts
└── tests/           # Test suites
```

## Design Principles

1. **Modularity**: Components should be loosely coupled
2. **Testability**: All code should be unit testable
3. **Documentation**: Code should be self-documenting
4. **Performance**: Optimize for scalability
5. **Security**: Follow security best practices

## API Architecture

- RESTful API design
- JSON request/response format
- JWT authentication
- Rate limiting
- Error handling with proper HTTP status codes

---

**Generated**: {datetime.utcnow().isoformat()}
**Framework**: Persona-Driven AI Framework v1.0.0
"""
        
        (self.rules_dir / "ARCHITECTURE.md").write_text(content)
        
    def _generate_coding_standards_md(self, project_info: Dict[str, Any]):
        """Generate CODING_STANDARDS.md context file"""
        
        tech_stack = project_info.get('tech_stack', [])
        
        # Determine primary language
        if 'Python' in tech_stack:
            language_standards = self._python_standards()
        elif 'TypeScript' in tech_stack or 'JavaScript' in tech_stack:
            language_standards = self._typescript_standards()
        else:
            language_standards = "Follow language-specific best practices"
        
        content = f"""# {project_info['name']} - Coding Standards

## Overview

This document defines coding standards and best practices for the {project_info['name']} project.

## General Principles

1. **Code Quality**: Write clean, readable, maintainable code
2. **Testing**: Aim for >80% code coverage
3. **Documentation**: Document all public APIs and complex logic
4. **Version Control**: Use meaningful commit messages
5. **Code Review**: All code must be reviewed before merging

## Language-Specific Standards

{language_standards}

## File Organization

- One class/component per file
- Group related files in directories
- Use index files for clean imports
- Keep files under 300 lines when possible

## Naming Conventions

- **Files**: `snake_case.py` or `kebab-case.ts`
- **Classes**: `PascalCase`
- **Functions**: `snake_case` (Python) or `camelCase` (TypeScript)
- **Constants**: `UPPER_SNAKE_CASE`
- **Variables**: `snake_case` (Python) or `camelCase` (TypeScript)

---

**Generated**: {datetime.utcnow().isoformat()}
**Framework**: Persona-Driven AI Framework v1.0.0
"""
        
        (self.rules_dir / "CODING_STANDARDS.md").write_text(content)

    def _generate_system_overview_md(self, project_info: Dict[str, Any]):
        """Generate SYSTEM_OVERVIEW.md"""
        content = f"""# {project_info['name']} - System Overview

## Project Information

- **Name**: {project_info['name']}
- **Description**: {project_info['description']}
- **Architecture**: {project_info.get('architecture_type', 'Not specified')}

## Technology Stack

{self._format_tech_stack(project_info.get('tech_stack', []))}

## Development Workflow

1. **Requirements**: Define feature requirements
2. **Architecture**: Design system architecture
3. **Planning**: Create implementation plan
4. **Development**: Implement features
5. **Testing**: Write and run tests
6. **Deployment**: Deploy to production

---

**Generated**: {datetime.utcnow().isoformat()}
**Framework**: Persona-Driven AI Framework v1.0.0
"""

        (self.rules_dir / "SYSTEM_OVERVIEW.md").write_text(content)

    def _generate_global_coverage_json(self, project_info: Dict[str, Any]):
        """Generate GLOBAL_COVERAGE.json metadata file"""
        coverage = {
            "contextBuilderAnalysis": {
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0.0",
                "repositoryInfo": {
                    "name": project_info['name'],
                    "type": project_info.get('architecture_type', 'application'),
                    "description": project_info['description'],
                    "techStack": project_info.get('tech_stack', [])
                }
            },
            "generatedFiles": {
                "coreFiles": [
                    "ARCHITECTURE.md",
                    "CODING_STANDARDS.md",
                    "SYSTEM_OVERVIEW.md"
                ]
            },
            "contextBuilderMetadata": {
                "executionMode": "bootstrap",
                "analysisDepth": "initial",
                "scopeCoverage": "basic",
                "validationStatus": "complete",
                "generationTimestamp": datetime.utcnow().isoformat()
            }
        }

        (self.rules_dir / "GLOBAL_COVERAGE.json").write_text(
            json.dumps(coverage, indent=2)
        )

    def _format_tech_stack(self, tech_stack: list) -> str:
        """Format technology stack as markdown list"""
        if not tech_stack:
            return "- Not specified"
        return "\n".join([f"- {tech}" for tech in tech_stack])

    def _python_standards(self) -> str:
        return """
### Python Standards

- Follow PEP 8 style guide
- Use type hints for all functions
- Use f-strings for string formatting
- Use list comprehensions when appropriate
- Use context managers for resource management
- Maximum line length: 100 characters

**Example**:
```python
def calculate_total(items: List[Dict[str, Any]]) -> float:
    \"\"\"Calculate total price of items.

    Args:
        items: List of item dictionaries with 'price' key

    Returns:
        Total price as float
    \"\"\"
    return sum(item['price'] for item in items)
```
"""

    def _typescript_standards(self) -> str:
        return """
### TypeScript Standards

- Use strict mode
- Define interfaces for all data structures
- Use const for immutable values
- Use async/await for asynchronous code
- Avoid 'any' type
- Maximum line length: 100 characters

**Example**:
```typescript
interface Item {
  name: string;
  price: number;
}

function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```
"""
