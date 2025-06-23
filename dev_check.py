#!/usr/bin/env python3
"""
Development validation script for NetBox Ping Plugin
Since this is a NetBox plugin, it doesn't run standalone.
This script validates the plugin structure and syntax.
"""

import sys
import os
import ast

def validate_python_files():
    """Validate Python syntax in all plugin files."""
    plugin_dir = 'netbox_ping'
    errors = []
    
    if not os.path.exists(plugin_dir):
        errors.append(f"Plugin directory '{plugin_dir}' not found")
        return errors
    
    for root, dirs, files in os.walk(plugin_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        source = f.read()
                    ast.parse(source)
                    print(f"✓ {file_path} - syntax OK")
                except SyntaxError as e:
                    error_msg = f"✗ {file_path} - Syntax Error: {e}"
                    errors.append(error_msg)
                    print(error_msg)
                except Exception as e:
                    error_msg = f"✗ {file_path} - Error: {e}"
                    errors.append(error_msg)
                    print(error_msg)
    
    return errors

def check_plugin_structure():
    """Check if required plugin files exist."""
    required_files = [
        'netbox_ping/__init__.py',
        'netbox_ping/plugin.py',
        'netbox_ping/models.py',
        'netbox_ping/views.py',
        'setup.py',
        'pyproject.toml'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} - exists")
        else:
            missing_files.append(file_path)
            print(f"✗ {file_path} - missing")
    
    return missing_files

def main():
    """Main validation function."""
    print("🔍 NetBox Ping Plugin Development Validation")
    print("=" * 50)
    
    print("\n📁 Checking plugin structure...")
    missing_files = check_plugin_structure()
    
    print("\n🐍 Validating Python syntax...")
    syntax_errors = validate_python_files()
    
    print("\n📋 Summary:")
    if missing_files:
        print(f"❌ Missing files: {len(missing_files)}")
        for file in missing_files:
            print(f"   - {file}")
    else:
        print("✅ All required files present")
    
    if syntax_errors:
        print(f"❌ Syntax errors: {len(syntax_errors)}")
        for error in syntax_errors:
            print(f"   - {error}")
    else:
        print("✅ No syntax errors found")
    
    print("\n💡 Note: This is a NetBox plugin. To test fully:")
    print("   1. Install NetBox (https://netboxlabs.com/docs/netbox/en/stable/)")
    print("   2. Install this plugin: pip install -e .")
    print("   3. Add 'netbox_ping' to PLUGINS in NetBox configuration")
    print("   4. Run NetBox development server: python manage.py runserver")
    
    # Keep the process running
    print("\n��� Development validation complete. Watching for changes...")
    print("Press Ctrl+C to exit.")
    
    try:
        import time
        while True:
            time.sleep(10)
            # Re-run validation every 10 seconds
            print("\n🔄 Re-validating...")
            validate_python_files()
    except KeyboardInterrupt:
        print("\n👋 Development validation stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
