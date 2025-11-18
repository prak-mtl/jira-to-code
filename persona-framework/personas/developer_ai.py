import google.generativeai as genai
from typing import Dict, Any
import os
from datetime import datetime
import re

class DeveloperAI:
    """
    Developer AI Persona - Generates code scaffolding and implementations
    from implementation plans.
    """
    
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        self.fallback_model = genai.GenerativeModel('models/gemini-1.5-flash')  # Lighter fallback
        self.persona_version = "v1.0.0"
        
    def generate_code(
        self, 
        task: Dict[str, str],
        architecture: str,
        coding_standards: str = None
    ) -> Dict[str, str]:
        """
        Generate code for a specific task
        
        Args:
            task: Task details from implementation plan
            architecture: SYSTEM_DESIGN.md content
            coding_standards: Optional coding standards
        
        Returns:
            Dictionary of {filename: code_content}
        """
        
        prompt = f"""
You are a Developer AI persona (v{self.persona_version}) - an expert Software Developer.

Your task is to generate production-ready code for the following task:

## Task Details:
{task}

## Architecture Context:
{architecture[:800]}...

## Coding Standards:
{coding_standards if coding_standards else "Follow Python PEP 8 / TypeScript best practices"}

Generate:
1. All necessary files (Python/TypeScript/JavaScript)
2. Complete implementations (not just stubs)
3. Proper error handling
4. Type hints/annotations
5. Docstrings/comments
6. Basic unit tests

Output format:
For each file, use this structure:
```filename: path/to/file.py
[code content]
```

Generate complete, working code that follows the architecture and coding standards.
Keep the code focused and concise.
"""

        # Configure generation settings
        generation_config = {
            'temperature': 0.7,
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 4096,
        }

        # Try primary model, fallback to lighter model if overloaded
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
        except Exception as e:
            error_str = str(e).lower()
            if "503" in str(e) or "overloaded" in error_str or "unavailable" in error_str:
                print("   ⚠️  Primary model overloaded, trying fallback model (gemini-1.5-flash)...")
                response = self.fallback_model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
            else:
                raise
        
        # Parse response to extract files
        files = {}

        # Handle multi-part responses
        try:
            content = response.text
        except ValueError:
            # Response has multiple parts, concatenate them
            content = ""
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if hasattr(part, 'text'):
                        content += part.text
        
        # Simple parsing - look for ```filename: pattern
        pattern = r'```filename:\s*(.+?)\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for filename, code in matches:
            files[filename.strip()] = code.strip()
        
        # If no files found with filename pattern, try generic code blocks
        if not files:
            generic_pattern = r'```(?:python|typescript|javascript|tsx|jsx)?\n(.*?)```'
            generic_matches = re.findall(generic_pattern, content, re.DOTALL)
            for i, code in enumerate(generic_matches):
                files[f'generated_code_{i}.py'] = code.strip()
        
        return files
    
    def generate_api_endpoint(
        self,
        endpoint_spec: Dict[str, Any],
        framework: str = "fastapi"
    ) -> str:
        """Generate API endpoint code"""
        
        prompt = f"""
Generate a {framework} API endpoint with the following specification:

{endpoint_spec}

Include:
- Request/response models (Pydantic)
- Endpoint handler function
- Error handling
- Input validation
- Docstrings

Return complete, production-ready code.
"""

        # Try primary model, fallback to lighter model if overloaded
        try:
            response = self.model.generate_content(prompt)
        except Exception as e:
            error_str = str(e).lower()
            if "503" in str(e) or "overloaded" in error_str or "unavailable" in error_str:
                print("   ⚠️  Primary model overloaded, trying fallback model (gemini-1.5-flash)...")
                response = self.fallback_model.generate_content(prompt)
            else:
                raise

        # Handle multi-part responses
        try:
            return response.text
        except ValueError:
            # Response has multiple parts, concatenate them
            content = ""
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if hasattr(part, 'text'):
                        content += part.text
            return content

