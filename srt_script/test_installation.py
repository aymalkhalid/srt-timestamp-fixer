#!/usr/bin/env python3
"""
SRT Timestamp Fixer - Installation Test

This script tests all components to ensure they're working correctly.
"""

import sys
import os

def test_basic_functionality():
    """Test core SRT processing functionality."""
    print("🧪 Testing Core Functionality...")
    
    try:
        # Import the core functions
        from convert_to_srt import analyze_timestamp_format, fix_timestamp_format
        
        # Test timestamp analysis
        test_cases = [
            ("00:01:30,500", False),  # Valid - should not need fixing
            ("01:30,500", True),      # Invalid - should need fixing
            ("1:30,500", True),       # Invalid - should need fixing
        ]
        
        for timestamp, should_need_fixing in test_cases:
            analysis = analyze_timestamp_format(timestamp)
            if analysis['needs_fixing'] == should_need_fixing:
                print(f"   ✅ {timestamp} -> {analysis['format_detected']}")
            else:
                print(f"   ❌ {timestamp} -> Expected needs_fixing={should_need_fixing}, got {analysis['needs_fixing']}")
                return False
        
        # Test timestamp fixing
        fixed = fix_timestamp_format("01:30,500")
        if fixed == "00:01:30,500":
            print(f"   ✅ Fixing: 01:30,500 -> {fixed}")
        else:
            print(f"   ❌ Fixing failed: Expected 00:01:30,500, got {fixed}")
            return False
        
        print("✅ Core functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        return False

def test_basic_gui():
    """Test basic GUI components."""
    print("\n🖥️  Testing Basic GUI...")
    
    try:
        import tkinter as tk
        
        # Try to create a basic window (don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()   # Clean up
        
        print("✅ Basic GUI (tkinter) is working!")
        return True
        
    except Exception as e:
        print(f"❌ Basic GUI test failed: {e}")
        return False

def test_modern_gui():
    """Test modern GUI components."""
    print("\n🎨 Testing Modern GUI...")
    
    try:
        import customtkinter as ctk
        
        # Try to create a modern window (don't show it)
        ctk.set_appearance_mode("dark")
        root = ctk.CTk()
        root.withdraw()  # Hide the window
        root.destroy()   # Clean up
        
        print("✅ Modern GUI (CustomTkinter) is working!")
        return True
        
    except ImportError:
        print("⚠️  Modern GUI not available - CustomTkinter not installed")
        print("   Install with: pip install customtkinter")
        return False
    except Exception as e:
        print(f"❌ Modern GUI test failed: {e}")
        return False

def test_web_app():
    """Test web application components."""
    print("\n🌐 Testing Web Application...")
    
    try:
        from flask import Flask
        
        # Try to create a basic Flask app
        app = Flask(__name__)
        
        print("✅ Web Application (Flask) is working!")
        return True
        
    except ImportError:
        print("⚠️  Web Application not available - Flask not installed")
        print("   Install with: pip install Flask")
        return False
    except Exception as e:
        print(f"❌ Web Application test failed: {e}")
        return False

def test_file_processing():
    """Test actual file processing with sample data."""
    print("\n📄 Testing File Processing...")
    
    try:
        from convert_to_srt import process_srt_file
        import tempfile
        import os
        
        # Create a temporary test file
        test_content = """1
00:00:00,500 --> 00:00:01,500
This is correct

2
01:30,500 --> 01:31,500
This needs fixing

3
00:00:02,500 --> 00:00:03,500
This is also correct
"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.srt') as input_file:
            input_file.write(test_content)
            input_path = input_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.srt') as output_file:
            output_path = output_file.name
        
        # Process the file
        stats = process_srt_file(input_path, output_path)
        
        # Check results
        if stats and stats['timestamp_lines_fixed'] == 1:
            print(f"   ✅ Processed {stats['total_lines']} lines")
            print(f"   ✅ Found {stats['timestamp_lines_found']} timestamp lines")
            print(f"   ✅ Fixed {stats['timestamp_lines_fixed']} problematic timestamps")
            
            # Read the output to verify fix
            with open(output_path, 'r') as f:
                output_content = f.read()
            
            if "00:01:30,500 --> 00:01:31,500" in output_content:
                print("   ✅ Timestamp correctly fixed: 01:30,500 -> 00:01:30,500")
            else:
                print("   ❌ Timestamp not fixed correctly")
                return False
        else:
            print(f"   ❌ Processing failed or unexpected results: {stats}")
            return False
        
        # Clean up
        os.unlink(input_path)
        os.unlink(output_path)
        
        print("✅ File processing test passed!")
        return True
        
    except Exception as e:
        print(f"❌ File processing test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🔧 SRT Timestamp Fixer - Installation Test")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print()
    
    results = []
    
    # Run all tests
    results.append(("Core Functionality", test_basic_functionality()))
    results.append(("Basic GUI", test_basic_gui()))
    results.append(("Modern GUI", test_modern_gui()))
    results.append(("Web Application", test_web_app()))
    results.append(("File Processing", test_file_processing()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your SRT Timestamp Fixer is ready to use!")
        print("\nYou can now run:")
        print("• python convert_to_srt.py           (CLI)")
        print("• python srt_fixer_gui.py           (Basic GUI)")
        print("• python srt_fixer_modern.py        (Modern GUI)")  
        print("• python srt_fixer_web.py           (Web App)")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the error messages above.")
        if passed >= 2:
            print("The basic functionality is working, so you can still use the available interfaces.")

if __name__ == "__main__":
    main()
