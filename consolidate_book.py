#!/usr/bin/env python3
"""
Script to consolidate all .tex files into a complete LaTeX book
Usage: python consolidate_book.py
Output: complete_book.tex
"""

import os
import glob

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

def read_file_content(filename):
    """Read content from a .tex file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        return content
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return ""

def consolidate_files():
    """Main function to consolidate all .tex files"""
    print("Starting consolidation process...")
    
    # Get all .tex files (numbered 1-205)
    tex_files = []
    for i in range(1, 206):
        filename = f"{i}.tex"
        if os.path.exists(filename):
            tex_files.append(filename)
        else:
            print(f"Warning: {filename} not found!")
    
    if not tex_files:
        print("Error: No .tex files found in current directory!")
        print("Make sure you run this script in the directory containing 1.tex, 2.tex, etc.")
        return
    
    print(f"Found {len(tex_files)} .tex files")
    
    # Create output file
    output_filename = "complete_book.tex"
    
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        # Write header
        print("Writing LaTeX header...")
        outfile.write(create_latex_header())
        
        # Process each file
        for i, filename in enumerate(tex_files, 1):
            print(f"Processing {filename} ({i}/{len(tex_files)})...")
            
            # Add chapter marker every file
            outfile.write(f"\n\\chapter*{{بخش {i}}}\n")
            outfile.write(f"\\addcontentsline{{toc}}{{chapter}}{{بخش {i}}}\n")
            outfile.write("\\label{chap:" + str(i) + "}\n\n")
            
            # Read and write content
            content = read_file_content(filename)
            if content:
                outfile.write(content)
                outfile.write("\n\n")
            else:
                outfile.write("\\textit{(این بخش خالی است)}\n\n")
            
            # Add page break after each section (optional)
            outfile.write("\\clearpage\n\n")
        
        # Write footer
        print("Writing LaTeX footer...")
        outfile.write(create_latex_footer())
    
    print(f"\n✓ Consolidation complete!")
    print(f"✓ Output file: {output_filename}")
    print(f"\nTo compile to PDF:")
    print(f"  xelatex {output_filename}")
    print(f"  xelatex {output_filename}  (run twice for TOC)")
    print(f"\nTo convert to Word:")
    print(f"  1. Compile to PDF first using xelatex")
    print(f"  2. Use pandoc: pandoc complete_book.tex -o complete_book.docx")
    print(f"  3. Or open the PDF in Word (Office 365) which has PDF import feature")
    print(f"  4. Or use online converters like pdf2docx")
    print(f"\nNote: Make sure XeLaTeX and Persian fonts are installed on your system")

if __name__ == "__main__":
    consolidate_files()
