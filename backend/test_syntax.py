#!/usr/bin/env python3
"""
Test script to check if all backend files have correct syntax
"""

import ast
import sys
import os

def check_syntax(file_path):
    """Check if a Python file has correct syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse the AST to check for syntax errors
        ast.parse(source)
        print(f"✅ {file_path} - Syntax OK")
        return True
    except SyntaxError as e:
        print(f"❌ {file_path} - Syntax Error: {e}")
        print(f"   Line {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"⚠️  {file_path} - Error: {e}")
        return False

def main():
    """Check all Python files in the backend"""
    backend_dir = "."
    python_files = []
    
    # Find all Python files
    for root, dirs, files in os.walk(backend_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"Checking {len(python_files)} Python files...")
    print("=" * 50)
    
    all_good = True
    for file_path in python_files:
        if not check_syntax(file_path):
            all_good = False
    
    print("=" * 50)
    if all_good:
        print("🎉 All files have correct syntax!")
    else:
        print("❌ Some files have syntax errors!")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
