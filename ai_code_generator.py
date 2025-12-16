# ai_code_generator.py
import openai
import os
import json
import logging
from flask import jsonify, request

class AICodeGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.setup_openai()
        
    def setup_openai(self):
        """Setup OpenAI client"""
        try:
            if self.api_key:
                openai.api_key = self.api_key
            else:
                logging.warning("OpenAI API key not found")
        except Exception as e:
            logging.error(f"OpenAI setup error: {e}")
    
    def generate_code(self, prompt, language='python', context=''):
        """Generate code using AI"""
        try:
            if not self.api_key:
                return self.generate_fallback_code(prompt, language)
            
            full_prompt = f"""
            Context: {context}
            Language: {language}
            Requirement: {prompt}
            
            Please generate clean, efficient code with proper comments.
            Return only the code without explanations.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert programmer."},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            generated_code = response.choices[0].message.content.strip()
            return {'status': 'success', 'code': generated_code, 'ai_used': True}
            
        except Exception as e:
            logging.error(f"AI Code Generation Error: {e}")
            # Fallback to template-based generation
            return self.generate_fallback_code(prompt, language)
    
    def generate_fallback_code(self, prompt, language):
        """Fallback code generation without AI"""
        templates = {
            'python': {
                'calculator': '''
def calculator(a, b, operation):
    """Simple calculator function"""
    if operation == 'add':
        return a + b
    elif operation == 'subtract':
        return a - b
    elif operation == 'multiply':
        return a * b
    elif operation == 'divide':
        return a / b if b != 0 else "Error: Division by zero"
    else:
        return "Error: Invalid operation"
''',
                'file_processor': '''
def process_file(filename):
    """Process file and return content"""
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Error: File not found"
    except Exception as e:
        return f"Error: {str(e)}"
'''
            },
            'javascript': {
                'calculator': '''
function calculator(a, b, operation) {
    switch(operation) {
        case 'add':
            return a + b;
        case 'subtract':
            return a - b;
        case 'multiply':
            return a * b;
        case 'divide':
            return b !== 0 ? a / b : "Error: Division by zero";
        default:
            return "Error: Invalid operation";
    }
}
''',
                'api_handler': '''
async function fetchData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}
'''
            }
        }
        
        # Simple keyword matching for fallback
        prompt_lower = prompt.lower()
        template_key = 'calculator' if any(word in prompt_lower for word in ['calculate', 'math', 'add', 'subtract']) else 'file_processor'
        
        if language in templates and template_key in templates[language]:
            return {
                'status': 'success', 
                'code': templates[language][template_key],
                'ai_used': False,
                'note': 'Fallback template used - add OpenAI API key for AI generation'
            }
        else:
            return {
                'status': 'error',
                'message': 'No template found for this request',
                'ai_used': False
            }
    
    def code_review(self, code, language='python'):
        """Provide code review suggestions"""
        try:
            suggestions = []
            
            # Basic code quality checks
            lines = code.split('\n')
            
            # Check for long lines
            for i, line in enumerate(lines, 1):
                if len(line) > 80:
                    suggestions.append(f"Line {i}: Consider breaking long line ({len(line)} characters)")
            
            # Check for basic Python patterns
            if language == 'python':
                if 'def ' in code and ':' in code and 'return' not in code:
                    suggestions.append("Function might be missing return statement")
                
                if 'try:' in code and 'except:' not in code:
                    suggestions.append("Try block without except clause")
            
            # Check for comments
            comment_lines = [line for line in lines if line.strip().startswith('#')]
            comment_ratio = len(comment_lines) / len(lines) if lines else 0
            if comment_ratio < 0.1:
                suggestions.append("Consider adding more comments for better documentation")
            
            return {
                'status': 'success',
                'suggestions': suggestions,
                'lines_of_code': len(lines),
                'comment_ratio': round(comment_ratio, 2)
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def generate_documentation(self, code, language='python'):
        """Generate basic documentation for code"""
        try:
            doc_lines = []
            lines = code.split('\n')
            
            doc_lines.append(f"# Code Documentation")
            doc_lines.append(f"Language: {language}")
            doc_lines.append(f"Total Lines: {len(lines)}")
            doc_lines.append("")
            
            # Extract function definitions
            for i, line in enumerate(lines):
                if line.strip().startswith('def '):
                    func_name = line.split('def ')[1].split('(')[0]
                    doc_lines.append(f"## Function: {func_name}")
                    doc_lines.append(f"Line: {i+1}")
                    doc_lines.append("")
                    # Look for docstring
                    if i + 1 < len(lines) and '"""' in lines[i+1]:
                        doc_lines.append("Description: " + lines[i+1].replace('"""', '').strip())
                    doc_lines.append("")
            
            return {
                'status': 'success',
                'documentation': '\n'.join(doc_lines)
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

# Flask routes integration
def setup_ai_code_routes(app, ai_system):
    @app.route('/api/ai/generate-code', methods=['POST'])
    def generate_code():
        data = request.get_json()
        prompt = data.get('prompt', '')
        language = data.get('language', 'python')
        context = data.get('context', '')
        
        result = ai_system.generate_code(prompt, language, context)
        return jsonify(result)
    
    @app.route('/api/ai/code-review', methods=['POST'])
    def code_review():
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        result = ai_system.code_review(code, language)
        return jsonify(result)
    
    @app.route('/api/ai/generate-docs', methods=['POST'])
    def generate_docs():
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        result = ai_system.generate_documentation(code, language)
        return jsonify(result)