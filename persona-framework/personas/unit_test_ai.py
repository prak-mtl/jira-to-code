import google.generativeai as genai
from typing import Dict, Any, List
import os
from datetime import datetime

class UnitTestAI:
    """
    Unit Test AI Persona - Generates comprehensive unit tests
    from implementation code and architecture.
    """
    
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        self.persona_version = "v1.0.0"
        
    def generate_unit_tests(
        self, 
        code_files: Dict[str, str],
        architecture: str,
        coding_standards: str = None,
        test_framework: str = "pytest"
    ) -> Dict[str, str]:
        """
        Generate comprehensive unit tests for code files
        
        Args:
            code_files: Dictionary of {filename: code_content}
            architecture: SYSTEM_DESIGN.md content for context
            coding_standards: Optional coding standards
            test_framework: Testing framework (pytest, jest, unittest)
        
        Returns:
            Dictionary of {test_filename: test_code}
        """
        
        test_files = {}
        
        for filename, code in list(code_files.items())[:3]:  # Limit to first 3 files
            prompt = f"""
You are a Unit Test AI persona (v{self.persona_version}) - an expert QA Engineer and Test Developer.

Your task is to generate comprehensive unit tests for the following code file.

## Code File: {filename}
```
{code[:1000]}...
```

## Architecture Context:
{architecture[:1000]}...

## Testing Requirements:
- Framework: {test_framework}
- Coverage: Aim for >80% code coverage
- Test all functions/methods
- Test edge cases and error scenarios
- Use mocking for external dependencies
- Include setup/teardown where needed
- Follow AAA pattern (Arrange, Act, Assert)

## Test Categories to Include:
1. **Happy Path Tests**: Normal operation scenarios
2. **Edge Case Tests**: Boundary conditions, empty inputs, null values
3. **Error Handling Tests**: Exception scenarios, invalid inputs
4. **Integration Points**: Mock external services/APIs
5. **Data Validation Tests**: Input validation, type checking

Generate complete, runnable unit tests with:
- Proper imports
- Test fixtures/setup
- Descriptive test names
- Clear assertions
- Mocking where appropriate
- Comments explaining complex test scenarios

Output the complete test file code.
Keep the tests focused and concise.
"""

            # Configure generation settings
            generation_config = {
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 4096,
            }

            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )

            # Handle multi-part responses
            try:
                test_code = response.text.strip()
            except ValueError:
                # Response has multiple parts, concatenate them
                test_code = ""
                for candidate in response.candidates:
                    for part in candidate.content.parts:
                        if hasattr(part, 'text'):
                            test_code += part.text
                test_code = test_code.strip()

            # Strip markdown code fences if present
            if test_code.startswith('```python'):
                test_code = test_code[len('```python'):].strip()
            elif test_code.startswith('```typescript') or test_code.startswith('```ts'):
                test_code = test_code[test_code.find('\n')+1:].strip()
            if test_code.startswith('```'):
                test_code = test_code[3:].strip()
            if test_code.endswith('```'):
                test_code = test_code[:-3].strip()

            # Determine test filename
            if filename.endswith('.py'):
                test_filename = filename.replace('.py', '_test.py')
                if not test_filename.startswith('test_'):
                    test_filename = 'test_' + test_filename
            elif filename.endswith('.ts') or filename.endswith('.tsx'):
                test_filename = filename.replace('.ts', '.test.ts').replace('.tsx', '.test.tsx')
            else:
                test_filename = f"test_{filename}"

            test_files[test_filename] = test_code
        
        return test_files
    
    def generate_test_summary(self, test_files: Dict[str, str]) -> str:
        """Generate TEST_SUMMARY.md documenting test coverage"""
        
        prompt = f"""
Generate a comprehensive TEST_SUMMARY.md document that includes:

1. **Test Coverage Overview**
   - Total test files: {len(test_files)}
   - Test categories covered
   - Estimated code coverage percentage

2. **Test Files Summary**
   For each test file, provide:
   - File name
   - Number of test cases
   - What is being tested
   - Coverage areas

3. **Testing Strategy**
   - Unit testing approach
   - Mocking strategy
   - Edge cases covered
   - Error scenarios tested

4. **Running Tests**
   - Commands to run tests
   - Expected output
   - CI/CD integration notes

## Test Files:
{chr(10).join([f"- {filename}" for filename in test_files.keys()])}

Generate a professional TEST_SUMMARY.md document.
"""

        response = self.model.generate_content(prompt)

        # Handle multi-part responses
        try:
            output = response.text.strip()
        except ValueError:
            # Response has multiple parts, concatenate them
            output = ""
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if hasattr(part, 'text'):
                        output += part.text
            output = output.strip()

        # Strip markdown code fences if present
        if output.startswith('```markdown'):
            output = output[len('```markdown'):].strip()
        if output.startswith('```'):
            output = output[3:].strip()
        if output.endswith('```'):
            output = output[:-3].strip()

        # Add AI generation footprint
        output += f"\n\n---\n\n## AI Generation Footprint\n\n"
        output += f"**Generated By**: Unit Test AI\n\n"
        output += f"**Framework Version**: {self.persona_version}\n\n"
        output += f"**Generation Date**: {datetime.utcnow().isoformat()} UTC\n\n"
        output += f"**Test Files Generated**: {len(test_files)}\n\n"
        output += f"---\n\n"
        output += f"Co-authored by Unit Test AI using Persona-Driven AI Framework {self.persona_version}\n"
        
        return output
    
    def validate_tests(self, test_code: str) -> Dict[str, Any]:
        """Validate generated test code quality"""
        validation = {
            "has_imports": "import " in test_code,
            "has_test_functions": "def test_" in test_code or "it(" in test_code,
            "has_assertions": "assert" in test_code or "expect(" in test_code,
            "has_mocking": "mock" in test_code.lower() or "patch" in test_code.lower(),
            "has_setup": "setUp" in test_code or "beforeEach" in test_code or "@pytest.fixture" in test_code,
            "line_count": len(test_code.split('\n')),
        }
        
        validation["is_valid"] = all([
            validation["has_imports"],
            validation["has_test_functions"],
            validation["has_assertions"],
            validation["line_count"] > 20
        ])
        
        return validation

