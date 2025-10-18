#!/usr/bin/env python3
"""
Diagnose the exact problem in complete_book.tex
This will show you exactly what's wrong at line 8165
"""

import os
import sys

def diagnose_complete_book():
    """Find the exact problem in complete_book.tex"""
    
    filename = "complete_book.tex"
    
    if not os.path.exists(filename):
        print(f"❌ {filename} not found!")
        print("   Run 'python consolidate_book.py' first")
        return 1
    
    print("=" * 70)
    print("Diagnosing complete_book.tex")
    print("=" * 70)
    print()
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    print(f"Total lines: {total_lines}")
    
    # Check if file ends properly
    last_10_lines = lines[-10:] if len(lines) >= 10 else lines
    print(f"\nLast 10 lines of file:")
    print("-" * 70)
    for i, line in enumerate(last_10_lines, start=len(lines)-len(last_10_lines)+1):
        print(f"{i:5d}: {line.rstrip()}")
    print("-" * 70)
    
    # Check for \end{document}
    full_content = ''.join(lines)
    
    has_begin = '\\begin{document}' in full_content
    has_end = '\\end{document}' in full_content
    
    print(f"\n\\begin{{document}} found: {'✓' if has_begin else '✗'}")
    print(f"\\end{{document}} found: {'✓' if has_end else '✗'}")
    
    if not has_end:
        print("\n❌ PROBLEM: Missing \\end{document}!")
        print("   The file doesn't have a proper ending")
        
        # Check if consolidate script added it
        if lines and lines[-1].strip() == '':
            print("   Last line is empty - footer may be missing")
        
        # Offer to fix
        print("\n" + "=" * 70)
        response = input("Add \\end{document} to the end? (yes/no): ").lower()
        
        if response in ['yes', 'y']:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write("\n\\end{document}\n")
            print("✓ Added \\end{document}")
            return 0
        else:
            print("No changes made")
            return 1
    
    # Check for brace balance
    open_count = full_content.count('{')
    close_count = full_content.count('}')
    
    print(f"\nBrace count:")
    print(f"  Opening: {open_count}")
    print(f"  Closing: {close_count}")
    print(f"  Balance: {open_count - close_count}")
    
    if open_count != close_count:
        print(f"\n❌ PROBLEM: Unbalanced braces!")
        diff = open_count - close_count
        
        if diff > 0:
            print(f"   Missing {diff} closing brace(s)")
            print("\n   Searching for the problematic line...")
            
            # Find where braces become unbalanced
            balance = 0
            for i, line in enumerate(lines, 1):
                for char in line:
                    if char == '{':
                        balance += 1
                    elif char == '}':
                        balance -= 1
                
                if balance < 0:
                    print(f"\n   Found problem at line {i}:")
                    start = max(0, i-5)
                    end = min(len(lines), i+5)
                    for j in range(start, end):
                        marker = ">>> " if j == i-1 else "    "
                        print(f"   {marker}{j+1:5d}: {lines[j].rstrip()}")
                    break
        else:
            print(f"   Extra {abs(diff)} closing brace(s)")
    
    # Check around line 8165 if file is long enough
    if len(lines) >= 8165:
        print(f"\nContext around line 8165 (where Pandoc failed):")
        print("-" * 70)
        start = max(0, 8163)
        end = min(len(lines), 8170)
        for i in range(start, end):
            marker = ">>> " if i == 8164 else "    "
            print(f"{marker}{i+1:5d}: {lines[i].rstrip()}")
        print("-" * 70)
    
    # Check for common LaTeX errors
    print("\nChecking for common LaTeX errors...")
    errors = []
    
    for i, line in enumerate(lines, 1):
        # Unclosed \begin
        if '\\begin{' in line and '\\end{' not in line:
            begin_env = line[line.find('\\begin{')+7:line.find('}', line.find('\\begin{'))]
            # Check if corresponding \end exists in next few lines
            found_end = False
            for j in range(i, min(i+50, len(lines))):
                if f'\\end{{{begin_env}}}' in lines[j]:
                    found_end = True
                    break
            if not found_end:
                errors.append(f"Line {i}: Unclosed \\begin{{{begin_env}}}")
        
        # Unmatched braces in line
        line_open = line.count('{')
        line_close = line.count('}')
        if line_open != line_close and abs(line_open - line_close) > 3:
            errors.append(f"Line {i}: Suspicious brace count (open:{line_open}, close:{line_close})")
    
    if errors:
        print(f"\nFound {len(errors)} potential errors:")
        for error in errors[:10]:
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors)-10} more")
    else:
        print("  No obvious errors found")
    
    print("\n" + "=" * 70)
    print("Diagnosis complete")
    print("=" * 70)
    
    return 0

if __name__ == "__main__":
    sys.exit(diagnose_complete_book())
