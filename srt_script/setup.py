#!/usr/bin/env python3
"""
SRT Timestamp Fixer - Installation and Setup Script

This script helps you set up and run the SRT Timestamp Fixer in different modes:
1. Command Line Interface (CLI)
2. Basic Desktop GUI (tkinter)
3. Modern Desktop GUI (CustomTkinter)
4. Web Application (Flask)

Author: AI Assistant
Date: June 24, 2025
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required.")
        print(f"   Your version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_package(package_name, description=""):
    """Install a Python package using pip."""
    try:
        print(f"📦 Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package_name}")
        if description:
            print(f"   {description}")
        return False

def check_package(package_name):
    """Check if a package is already installed."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def setup_basic_gui():
    """Set up basic GUI (tkinter is built-in)."""
    print("\n🖥️  Setting up Basic Desktop GUI...")
    print("✅ tkinter is built into Python - no additional packages needed")
    return True

def setup_modern_gui():
    """Set up modern GUI with CustomTkinter."""
    print("\n🎨 Setting up Modern Desktop GUI...")
    
    packages = [
        ("customtkinter", "Modern tkinter replacement with better styling"),
        ("Pillow", "Image processing library for icons and themes")
    ]
    
    success = True
    for package, description in packages:
        if not check_package(package.lower().replace("-", "_")):
            if not install_package(package, description):
                success = False
        else:
            print(f"✅ {package} already installed")
    
    return success

def setup_web_app():
    """Set up web application with Flask."""
    print("\n🌐 Setting up Web Application...")
    
    packages = [
        ("Flask", "Web framework for the browser-based interface"),
        ("Werkzeug", "WSGI utility library (usually comes with Flask)")
    ]
    
    success = True
    for package, description in packages:
        package_check = package.lower().replace("-", "_")
        if not check_package(package_check):
            if not install_package(package, description):
                success = False
        else:
            print(f"✅ {package} already installed")
    
    return success

def create_launcher_scripts():
    """Create launcher scripts for easy access."""
    print("\n📝 Creating launcher scripts...")
    
    current_dir = Path(__file__).parent
    
    # CLI launcher
    cli_script = f'''#!/bin/bash
# SRT Timestamp Fixer - Command Line Interface
cd "{current_dir}"
python convert_to_srt.py
'''
    
    # Basic GUI launcher
    gui_script = f'''#!/bin/bash
# SRT Timestamp Fixer - Basic Desktop GUI
cd "{current_dir}"
python srt_fixer_gui.py
'''
    
    # Modern GUI launcher
    modern_script = f'''#!/bin/bash
# SRT Timestamp Fixer - Modern Desktop GUI
cd "{current_dir}"
python srt_fixer_modern.py
'''
    
    # Web app launcher
    web_script = f'''#!/bin/bash
# SRT Timestamp Fixer - Web Application
cd "{current_dir}"
echo "Starting SRT Timestamp Fixer Web App..."
echo "Open your browser and go to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
python srt_fixer_web.py
'''
    
    launchers = [
        ("launch_cli.sh", cli_script),
        ("launch_gui.sh", gui_script),
        ("launch_modern.sh", modern_script),
        ("launch_web.sh", web_script)
    ]
    
    for filename, content in launchers:
        filepath = current_dir / filename
        with open(filepath, 'w') as f:
            f.write(content)
        
        # Make executable on Unix-like systems
        if os.name != 'nt':  # Not Windows
            os.chmod(filepath, 0o755)
        
        print(f"✅ Created {filename}")

def show_usage_instructions():
    """Show instructions for using the different interfaces."""
    print("\n" + "="*60)
    print("🎉 INSTALLATION COMPLETE!")
    print("="*60)
    print("\nYou now have 4 ways to use the SRT Timestamp Fixer:")
    print()
    
    print("1️⃣  COMMAND LINE INTERFACE:")
    print("   • Run: python convert_to_srt.py")
    print("   • Or: ./launch_cli.sh")
    print("   • Best for: Automation, scripting, power users")
    print()
    
    print("2️⃣  BASIC DESKTOP GUI:")
    print("   • Run: python srt_fixer_gui.py")
    print("   • Or: ./launch_gui.sh")
    print("   • Best for: Simple, reliable desktop interface")
    print()
    
    print("3️⃣  MODERN DESKTOP GUI:")
    print("   • Run: python srt_fixer_modern.py")
    print("   • Or: ./launch_modern.sh")
    print("   • Best for: Beautiful, modern desktop experience")
    print("   • Requires: customtkinter package")
    print()
    
    print("4️⃣  WEB APPLICATION:")
    print("   • Run: python srt_fixer_web.py")
    print("   • Or: ./launch_web.sh")
    print("   • Then open: http://localhost:5000")
    print("   • Best for: Browser-based, cross-platform access")
    print("   • Requires: Flask package")
    print()
    
    print("📁 FILES IN YOUR DIRECTORY:")
    print("   • convert_to_srt.py     - Core CLI script")
    print("   • srt_fixer_gui.py      - Basic desktop GUI")
    print("   • srt_fixer_modern.py   - Modern desktop GUI")
    print("   • srt_fixer_web.py      - Web application")
    print("   • setup.py              - This setup script")
    print()
    
    print("🔧 WHAT IT FIXES:")
    print("   • Missing hours: 01:30,500 → 00:01:30,500")
    print("   • Missing arrows: 01:30,500  01:31,500 → 00:01:30,500 --> 00:01:31,500")
    print("   • Inconsistent timestamp formatting")
    print()
    
    print("💡 TIP: Start with the Basic Desktop GUI if you're unsure!")

def main():
    """Main setup function."""
    print("🔧 SRT Timestamp Fixer - Setup & Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    print("\nChoose installation options:")
    print("1. Basic setup (CLI + Basic GUI)")
    print("2. Full setup (All interfaces)")
    print("3. Custom setup (Choose components)")
    print("4. Just create launcher scripts")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            print("\n📦 Basic Setup - Installing CLI and Basic GUI...")
            setup_basic_gui()
            create_launcher_scripts()
            break
            
        elif choice == "2":
            print("\n📦 Full Setup - Installing all components...")
            setup_basic_gui()
            setup_modern_gui()
            setup_web_app()
            create_launcher_scripts()
            break
            
        elif choice == "3":
            print("\n📦 Custom Setup...")
            components = []
            
            if input("Install Modern GUI? (y/n): ").lower().startswith('y'):
                components.append("modern")
            
            if input("Install Web App? (y/n): ").lower().startswith('y'):
                components.append("web")
            
            setup_basic_gui()  # Always include basic
            
            if "modern" in components:
                setup_modern_gui()
            
            if "web" in components:
                setup_web_app()
            
            create_launcher_scripts()
            break
            
        elif choice == "4":
            print("\n📝 Creating launcher scripts only...")
            create_launcher_scripts()
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
    
    show_usage_instructions()

if __name__ == "__main__":
    main()
