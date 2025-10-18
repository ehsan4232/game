#!/usr/bin/env python3
"""
Script to consolidate all .tex files into a complete LaTeX book
Usage: python consolidate_book.py
Output: complete_book.tex
"""

import os
import re

def create_latex_header():
    """Create the LaTeX document header with Persian support"""
    header = r"""\documentclass[12pt,a4paper]{book}

% Essential packages for Persian/Farsi text
\usepackage{xepersian}

% Set Persian fonts - you can change these to fonts installed on your system
% Common Persian fonts: XB Niloofar, XB Zar, XB Roya, XB Nazanin, Nazli, Lotus, Iranian Sans
\settextfont[Scale=1]{XB Niloofar}
\setlatintextfont[Scale=1]{Times New Roman}

% Page geometry
\usepackage{geometry}
\geometry{
    a4paper,
    left=2.5cm,
    right=2.5cm,
    top=3cm,
    bottom=3cm
}

% Graphics support
\usepackage{graphicx}

% Hyperlinks
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,
    urlcolor=cyan,
    pdftitle={کتاب کامل},
    pdfauthor={مترجم},
    pdfsubject={کتاب ترجمه شده},
    pdfkeywords={کتاب، ترجمه، فارسی},
    bookmarksnumbered=true,
    pdfstartview=FitH
}

% Line spacing
\usepackage{setspace}
\onehalfspacing

% Better paragraph spacing
\setlength{\parskip}{0.5em}
\setlength{\parindent}{1.5em}

% Chapter and section formatting
\usepackage{titlesec}
\titleformat{\chapter}[display]
{\normalfont\huge\bfseries\centering}{\chaptertitlename\ \thechapter}{20pt}{\Huge}
\titlespacing*{\chapter}{0pt}{-20pt}{40pt}

% Footnote support
\usepackage{footnote}

% Better table support
\usepackage{longtable}
\usepackage{booktabs}

% List spacing
\usepackage{enumitem}

\begin{document}

% Title page
\begin{titlepage}
    \centering
    \vspace*{3cm}
    
    {\Huge\bfseries کتاب کامل\par}
    \vspace{1.5cm}
    
    {\Large\itshape مجموعه کامل متن‌های ترجمه شده\par}
    \vspace{2cm}
    
    {\large نسخه جامع و یکپارچه\par}
    \vfill
    
    {\large تاریخ تهیه: \today\par}
\end{titlepage}

% Table of contents
\tableofcontents
\cleardoublepage

% Main content starts here
"""
    return header

def create_latex_footer():
    """Create the LaTeX document footer"""
    footer = r"""
\end{document}
"""
    return footer

def clean_latex_content(content):
    """Clean content to avoid LaTeX errors"""
    if not content:
        return ""
    
    # Remove any stray \end{document} or \begin{document} commands
    content = re.sub(r'\\end\{document\}', '', content)
    content = re.sub(r'\\begin\{document\}', '', content)
    
    # Escape special LaTeX characters that aren't already escaped
    # But be careful not to escape already escaped characters or LaTeX commands
    
    # Remove multiple consecutive blank lines (keep max 2)
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    return content

def read_file_content(filename):
    """Read content from a .tex file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        return clean_latex_content(content)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return ""

def consolidate_files():
    """Main function to consolidate all .tex files"""
    print("Starting consolidation process...")
    print("=" * 60)
    
    # Get all .tex files (numbered 1-205)
    tex_files = []
    missing_files = []
    
    for i in range(1, 206):
        filename = f"{i}.tex"
        if os.path.exists(filename):
            tex_files.append(filename)
        else:
            missing_files.append(filename)
    
    if not tex_files:
        print("❌ Error: No .tex files found in current directory!")
        print("Make sure you run this script in the directory containing 1.tex, 2.tex, etc.")
        return
    
    print(f"✓ Found {len(tex_files)} .tex files")
    if missing_files:
        print(f"⚠ Warning: {len(missing_files)} files are missing")
        print(f"  Missing: {', '.join(missing_files[:10])}" + ("..." if len(missing_files) > 10 else ""))
    
    print("=" * 60)
    
    # Create output file
    output_filename = "complete_book.tex"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            # Write header
            print("📝 Writing LaTeX header...")
            outfile.write(create_latex_header())
            
            # Process each file
            for i, filename in enumerate(tex_files, 1):
                file_num = int(filename.replace('.tex', ''))
                print(f"📄 Processing {filename} ({i}/{len(tex_files)})...", end=' ')
                
                # Add chapter marker every file
                outfile.write(f"\n% ==== File: {filename} ====\n")
                outfile.write(f"\\chapter*{{بخش {file_num}}}\n")
                outfile.write(f"\\addcontentsline{{toc}}{{chapter}}{{بخش {file_num}}}\n")
                outfile.write("\\label{chap:" + str(file_num) + "}\n\n")
                
                # Read and write content
                content = read_file_content(filename)
                if content:
                    outfile.write(content)
                    outfile.write("\n\n")
                    print("✓")
                else:
                    outfile.write("\\textit{(این بخش خالی است)}\n\n")
                    print("⚠ Empty")
                
                # Add page break after each section
                outfile.write("\\clearpage\n\n")
            
            # Write footer
            print("\n📝 Writing LaTeX footer...")
            outfile.write(create_latex_footer())
        
        print("=" * 60)
        print(f"✅ Consolidation complete!")
        print(f"✅ Output file: {output_filename}")
        
        # Verify the file
        with open(output_filename, 'r', encoding='utf-8') as f:
            content = f.read()
            if '\\begin{document}' in content and '\\end{document}' in content:
                print("✅ File structure verified: \\begin{document} and \\end{document} found")
            else:
                print("⚠ Warning: File structure may be incomplete")
        
        print("\n" + "=" * 60)
        print("📚 Next Steps:")
        print("\n1️⃣  To compile to PDF:")
        print(f"     xelatex {output_filename}")
        print(f"     xelatex {output_filename}  (run twice for TOC)")
        
        print("\n2️⃣  To convert to Word (.docx):")
        print("   Method A - Using Pandoc (Simple conversion):")
        print(f"     pandoc {output_filename} -s -o game.docx")
        
        print("\n   Method B - Via PDF (Better formatting):")
        print(f"     xelatex {output_filename}")
        print("     Then open complete_book.pdf in Microsoft Word")
        
        print("\n   Method C - Using Pandoc with better options:")
        print(f"     pandoc {output_filename} -s --toc -o game.docx")
        
        print("\n3️⃣  Requirements:")
        print("     • For PDF: Install XeLaTeX (part of TeX Live or MiKTeX)")
        print("     • For Word: Install Pandoc from https://pandoc.org")
        print("     • Persian fonts must be installed (XB Niloofar recommended)")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during consolidation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    consolidate_files()
