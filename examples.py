"""
Examples of using diff2latex as a library.
"""

def example_simple_usage():
    """Example of the simplest way to use diff2latex."""
    import diff2latex
    
    # Simple diff content
    diff_content = """--- file1.txt	2025-01-01 00:00:00.000000000 +0000
+++ file2.txt	2025-01-01 00:00:01.000000000 +0000
@@ -1,3 +1,3 @@
 line 1
-old line 2
+new line 2
 line 3
"""
    
    # Convert to LaTeX using the convenience function
    latex_output = diff2latex.diff_to_latex(
        diff_content,
        highlight_style="github",
        file_extension=".txt"
    )
    
    print("Generated LaTeX:")
    print(latex_output[:200] + "...")


def example_file_processing():
    """Example of processing a diff file."""
    import diff2latex
    
    # Process a diff file directly
    latex_output = diff2latex.diff_file_to_latex(
        "example.diff",
        output_path="output.tex",
        font_family="Monaco",
        highlight_style="monokai"
    )
    
    print("LaTeX written to output.tex")


def example_pdf_generation():
    """Example of creating a PDF directly."""
    import diff2latex
    
    diff_content = """--- old.py
+++ new.py
@@ -1,5 +1,5 @@
 def hello():
-    print("Hello, World!")
+    print("Hello, diff2latex!")
 
 if __name__ == "__main__":
     hello()
"""
    
    # Create PDF directly
    diff2latex.create_diff_pdf(
        diff_content,
        "my_diff.pdf",
        highlight_style="github",
        file_extension=".py"
    )
    
    print("PDF created: my_diff.pdf")


def example_class_based_processing():
    """Example using the class-based DiffProcessor."""
    import diff2latex
    
    # Create a processor with specific settings
    processor = diff2latex.DiffProcessor(
        font_family="Source Code Pro",
        font_size="9pt",
        highlight_style="vs",
        file_extension=".cpp"
    )
    
    # Process multiple diffs with the same settings
    diff1 = """--- old.cpp
+++ new.cpp
@@ -1,3 +1,3 @@
 #include <iostream>
-std::cout << "Hello" << std::endl;
+std::cout << "Hello, World!" << std::endl;
"""
    
    diff2 = """--- old.cpp
+++ new.cpp  
@@ -1,3 +1,3 @@
 int main() {
-    return 0;
+    return EXIT_SUCCESS;
 }
"""
    
    latex1 = processor.process(diff1)
    latex2 = processor.process(diff2)
    
    # Create PDFs
    processor.create_pdf(diff1, "diff1.pdf")
    processor.create_pdf(diff2, "diff2.pdf")
    
    print("Processed multiple diffs with consistent styling")


def example_low_level_access():
    """Example using the low-level classes directly."""
    import diff2latex
    from io import StringIO
    
    # Access the core classes directly
    colorizer = diff2latex.CharColorizer(
        style_name="github",
        ext=".py"
    )
    
    diff_content = """--- test.py
+++ test.py
@@ -1,2 +1,2 @@
-x = 1
+x = 2
"""
    
    # Use the core Diff2Latex class
    diff_io = StringIO(diff_content)
    differ = diff2latex.Diff2Latex.build(diff_io, colorizer=colorizer)
    latex_lines = differ.to_latex()
    
    print("Raw LaTeX content:")
    print(latex_lines)
    
    # You can also work with individual models
    # CodeBlock, Cell, Line classes are also available


def example_all_import_styles():
    """Show different ways to import and use the library."""
    
    # Style 1: Import everything from main package
    import diff2latex
    latex1 = diff2latex.diff_to_latex("diff content")
    
    # Style 2: Import specific functions
    from diff2latex import diff_to_latex, create_diff_pdf
    latex2 = diff_to_latex("diff content")
    
    # Style 3: Import classes for advanced usage
    from diff2latex import Diff2Latex, CharColorizer
    colorizer = CharColorizer(style_name="github")
    
    # Style 4: Import the processor class
    from diff2latex import DiffProcessor
    processor = DiffProcessor(highlight_style="monokai")
    
    print("All import styles work!")


if __name__ == "__main__":
    print("=== diff2latex Library Usage Examples ===\n")
    
    try:
        print("1. Simple Usage:")
        example_simple_usage()
        print()
        
        print("2. All Import Styles:")
        example_all_import_styles()
        print()
        
        print("3. Low-level Access:")
        example_low_level_access()
        print()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure diff2latex is installed: pip install diff2latex")
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Some examples may require additional setup (diff files, lualatex, etc.)")
