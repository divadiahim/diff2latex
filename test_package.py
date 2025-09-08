#!/usr/bin/env python3
"""Basic smoke test for diff2latex package."""

import sys
import subprocess
import tempfile
import os

def test_import():
    """Test that the package can be imported."""
    try:
        import diff2latex
        print("✓ Package imports successfully")
        print(f"✓ Version: {diff2latex.__version__}")
        
        # Test that all main classes are available
        expected_classes = [
            'Diff2Latex', 'CharColorizer', 'ColorMap',
            'CodeBlock', 'Cell', 'Line',
            'diff_to_latex', 'diff_file_to_latex', 'create_diff_pdf', 'DiffProcessor'
        ]
        
        missing = []
        for cls_name in expected_classes:
            if not hasattr(diff2latex, cls_name):
                missing.append(cls_name)
        
        if missing:
            print(f"✗ Missing classes/functions: {missing}")
            return False
        else:
            print("✓ All expected classes and functions are available")
            return True
            
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_convenience_api():
    """Test the convenience API."""
    try:
        import diff2latex
        
        # Test simple diff processing
        diff_content = """--- file1.txt	2025-01-01 00:00:00.000000000 +0000
+++ file2.txt	2025-01-01 00:00:01.000000000 +0000
@@ -1,3 +1,3 @@
 line 1
-old line 2
+new line 2
 line 3
"""
        
        # Test the convenience function
        latex_output = diff2latex.diff_to_latex(diff_content)
        
        if latex_output and "line 1" in latex_output and "new line 2" in latex_output:
            print("✓ Convenience API works")
            return True
        else:
            print("✗ Convenience API failed to produce expected output")
            return False
            
    except Exception as e:
        print(f"✗ Convenience API test failed: {e}")
        return False


def test_class_based_processor():
    """Test the class-based DiffProcessor."""
    try:
        from diff2latex import DiffProcessor
        
        processor = DiffProcessor(
            font_family="Monaco",
            highlight_style=None,  # No highlighting to avoid dependency issues
        )
        
        diff_content = """--- test.txt
+++ test.txt
@@ -1,2 +1,2 @@
-old text
+new text
"""
        
        latex_output = processor.process(diff_content)
        
        if latex_output and "old text" in latex_output and "new text" in latex_output:
            print("✓ Class-based processor works")
            return True
        else:
            print("✗ Class-based processor failed")
            return False
            
    except Exception as e:
        print(f"✗ Class-based processor test failed: {e}")
        return False

def test_cli_help():
    """Test that the CLI shows help."""
    try:
        result = subprocess.run([sys.executable, "-m", "diff2latex", "--help"], 
                              capture_output=True, text=True)
        if result.returncode == 0 and "diff2latex" in result.stdout:
            print("✓ CLI help works")
            return True
        else:
            print(f"✗ CLI help failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        return False

def test_basic_functionality():
    """Test basic diff processing."""
    try:
        # Create a simple diff file
        diff_content = """--- file1.txt	2025-01-01 00:00:00.000000000 +0000
+++ file2.txt	2025-01-01 00:00:01.000000000 +0000
@@ -1,3 +1,3 @@
 line 1
-old line 2
+new line 2
 line 3
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.diff', delete=False) as f:
            f.write(diff_content)
            diff_file = f.name
        
        with tempfile.TemporaryDirectory() as output_dir:
            # Test the build command
            result = subprocess.run([
                sys.executable, "-m", "diff2latex", 
                "build", diff_file, output_dir
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                tex_file = os.path.join(output_dir, "diff_output.tex")
                if os.path.exists(tex_file):
                    print("✓ Basic diff processing works")
                    return True
                else:
                    print(f"✗ Output file not created")
                    return False
            else:
                print(f"✗ Build command failed: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False
    finally:
        if 'diff_file' in locals():
            os.unlink(diff_file)

def main():
    """Run all tests."""
    print("🧪 Running diff2latex smoke tests...\n")
    
    tests = [
        test_import,
        test_convenience_api, 
        test_class_based_processor,
        test_cli_help,
        test_basic_functionality,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Package is ready.")
        return 0
    else:
        print("❌ Some tests failed. Please fix before publishing.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
