#!/usr/bin/env python3
"""
Comprehensive LaTeX file checker and fixer
This script will check all .tex files for common problems and fix them

Run this script in your output/game directory
"""

import os
import sys

def count_braces(text):
    """Count opening and closing braces"""
    open_count = text.count('{')
    close_count = text.count('}')
    return open_count, close_count

def check_file(filename):
    """Check a single file for problems"""
    problems = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check 1: Brace balance
        open_br, close_br = count_braces(content)
        if open_br != close_br:
            problems.append(f"Unbalanced braces: {open_br} open, {close_br} close (diff: {open_br - close_br})")
        
        # Check 2: Stray document commands
        if '\\end{document}' in content:
            problems.append("Contains \\end{document}")
        if '\\begin{document}' in content:
            problems.append("Contains \\begin{document}")
        
        # Check 3: Empty file
        if len(content.strip()) == 0:
            problems.append("Empty file")
        
        # Check 4: File ends abruptly (incomplete sentence)
        if content.strip() and not content.strip()[-1] in '.!?»)}]"\'':
            last_20 = content.strip()[-20:]
            problems.append(f"May end abruptly: ...{last_20}")
        
        return content, problems
    
    except Exception as e:
        return None, [f"Error reading file: {e}"]

def fix_file(filename, content, problems):
    """Fix problems in a file"""
    fixed_content = content
    fixes_applied = []
    
    for problem in problems:
        if "Unbalanced braces" in problem:
            open_br, close_br = count_braces(fixed_content)
            diff = open_br - close_br
            
            if diff > 0:
                # Add missing closing braces
                fixed_content = fixed_content.rstrip() + ('}' * diff)
                fixes_applied.append(f"Added {diff} closing brace(s)")
            elif diff < 0:
                # Remove extra closing braces from end
                fixed_content = fixed_content.rstrip()
                while diff < 0 and fixed_content.endswith('}'):
                    fixed_content = fixed_content[:-1].rstrip()
                    diff += 1
                fixes_applied.append(f"Removed {abs(diff)} extra closing brace(s)")
        
        elif "\\end{document}" in problem:
            fixed_content = fixed_content.replace('\\end{document}', '')
            fixes_applied.append("Removed \\end{document}")
        
        elif "\\begin{document}" in problem:
            fixed_content = fixed_content.replace('\\begin{document}', '')
            fixes_applied.append("Removed \\begin{document}")
    
    return fixed_content, fixes_applied

def main():
    """Main function"""
    print("=" * 70)
    print("LaTeX File Checker and Fixer")
    print("=" * 70)
    print()
    
    # Find all .tex files
    tex_files = []
    for i in range(1, 206):
        filename = f"{i}.tex"
        if os.path.exists(filename):
            tex_files.append(filename)
    
    if not tex_files:
        print("❌ No .tex files found!")
        print("   Make sure you're in the correct directory")
        return 1
    
    print(f"Found {len(tex_files)} .tex files\n")
    
    # Check all files
    files_with_problems = []
    total_problems = 0
    
    print("Checking files...")
    print("-" * 70)
    
    for filename in tex_files:
        content, problems = check_file(filename)
        
        if problems:
            files_with_problems.append((filename, content, problems))
            total_problems += len(problems)
            print(f"❌ {filename}: {len(problems)} problem(s)")
            for p in problems:
                print(f"   - {p}")
        else:
            print(f"✓ {filename}: OK")
    
    print("-" * 70)
    print(f"\nTotal: {len(files_with_problems)} files with {total_problems} problems")
    
    if not files_with_problems:
        print("\n✅ All files are OK!")
        return 0
    
    # Ask to fix
    print("\n" + "=" * 70)
    response = input("Do you want to fix these problems? (yes/no): ").lower()
    
    if response not in ['yes', 'y']:
        print("No changes made.")
        return 0
    
    # Fix files
    print("\nFixing files...")
    print("-" * 70)
    
    fixed_count = 0
    for filename, content, problems in files_with_problems:
        fixed_content, fixes = fix_file(filename, content, problems)
        
        if fixes:
            # Save fixed file
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"✓ {filename}: Fixed")
                for fix in fixes:
                    print(f"   - {fix}")
                fixed_count += 1
            except Exception as e:
                print(f"❌ {filename}: Failed to save - {e}")
        else:
            print(f"⚠ {filename}: No fixes applied")
    
    print("-" * 70)
    print(f"\n✅ Fixed {fixed_count} files")
    print("\nYou can now run:")
    print("  python consolidate_book.py")
    print("  pandoc complete_book.tex -s -o game.docx")
    print("=" * 70)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
