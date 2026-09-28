#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import argparse
import shutil
from datetime import datetime

def remove_comments_from_line(line):
    """
    Remove comments from a line while preserving strings and docstrings
    """
    stripped = line.strip()
    if stripped.startswith('"""') or stripped.startswith("'''"):
        return line
    
    # Handle different comment scenarios
    in_string = False
    in_double_quote = False
    in_single_quote = False
    escape_next = False
    i = 0
    
    while i < len(line):
        char = line[i]
        
        if escape_next:
            escape_next = False
            i += 1
            continue
            
        if char == '\\':
            escape_next = True
            i += 1
            continue
            
        if char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
            in_string = in_double_quote or in_single_quote
        elif char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            in_string = in_double_quote or in_single_quote
        elif char == '#' and not in_string:
            # Found comment outside of string, remove it
            return line[:i].rstrip() + '\n' if line.endswith('\n') else line[:i].rstrip()
            
        i += 1
    
    return line

def is_docstring_line(line, in_docstring, docstring_type):
    """
    Check if line is part of a docstring
    """
    stripped = line.strip()
    
    # Check for docstring start/end
    if '"""' in line:
        if not in_docstring:
            return True, True, '"""'
        elif docstring_type == '"""':
            return True, False, None
    elif "'''" in line:
        if not in_docstring:
            return True, True, "'''"
        elif docstring_type == "'''":
            return True, False, None
    
    return in_docstring, in_docstring, docstring_type

def clean_python_file(file_path, preserve_docstrings=True, preserve_shebang=True):
    """
    Clean comments from a Python file
    
    Args:
        file_path: Path to the Python file
        preserve_docstrings: Whether to keep docstrings
        preserve_shebang: Whether to keep shebang lines
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # Try with different approach for Python 2
        import codecs
        with codecs.open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        # Fallback for Python 2
        with open(file_path, 'r') as f:
            lines = f.readlines()
    
    cleaned_lines = []
    in_docstring = False
    docstring_type = None
    
    for i, line in enumerate(lines):
        # Preserve shebang
        if i == 0 and preserve_shebang and line.startswith('#!'):
            cleaned_lines.append(line)
            continue
        
        # Preserve encoding declarations
        if i <= 1 and re.match(r'#.*?coding[:=]', line):
            cleaned_lines.append(line)
            continue
        
        # Handle docstrings
        if preserve_docstrings:
            is_docstring, in_docstring, docstring_type = is_docstring_line(line, in_docstring, docstring_type)
            if is_docstring:
                cleaned_lines.append(line)
                continue
        
        # Remove comments from regular lines
        if not in_docstring:
            cleaned_line = remove_comments_from_line(line)
            # Only add non-empty lines or lines that contain code
            if cleaned_line.strip() or (not cleaned_line.strip() and line.strip() == ''):
                cleaned_lines.append(cleaned_line)
        else:
            # Inside docstring, keep the line
            cleaned_lines.append(line)
    
    return cleaned_lines

def cleanup_directory(directory, backup=True, preserve_docstrings=True, preserve_shebang=True):
    """
    Clean all Python files in a directory
    """
    processed_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                print("Processing: %s" % file_path)
                
                # Create backup if requested
                if backup:
                    backup_path = file_path + ".backup_%s" % datetime.now().strftime('%Y%m%d_%H%M%S')
                    shutil.copy2(file_path, backup_path)
                    print("  Backup created: %s" % backup_path)
                
                try:
                    # Clean the file
                    cleaned_lines = clean_python_file(file_path, preserve_docstrings, preserve_shebang)
                    
                    # Write cleaned content back
                    with open(file_path, 'w') as f:
                        f.writelines(cleaned_lines)
                    
                    processed_files.append(file_path)
                    print("  ✓ Cleaned successfully")
                    
                except Exception as e:
                    print("  ✗ Error processing file: %s" % str(e))
    
    return processed_files

def main():
    parser = argparse.ArgumentParser(description='Clean comments from Python files')
    parser.add_argument('path', help='File or directory path to clean')
    parser.add_argument('--no-backup', action='store_true', help='Don\'t create backup files')
    parser.add_argument('--remove-docstrings', action='store_true', help='Also remove docstrings')
    parser.add_argument('--remove-shebang', action='store_true', help='Also remove shebang lines')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print("Error: Path '%s' does not exist" % args.path)
        return
    
    backup = not args.no_backup
    preserve_docstrings = not args.remove_docstrings
    preserve_shebang = not args.remove_shebang
    
    if os.path.isfile(args.path):
        # Single file
        if args.path.endswith('.py'):
            print("Processing single file: %s" % args.path)
            
            if backup:
                backup_path = args.path + ".backup_%s" % datetime.now().strftime('%Y%m%d_%H%M%S')
                shutil.copy2(args.path, backup_path)
                print("Backup created: %s" % backup_path)
            
            try:
                cleaned_lines = clean_python_file(args.path, preserve_docstrings, preserve_shebang)
                with open(args.path, 'w') as f:
                    f.writelines(cleaned_lines)
                print("✓ File cleaned successfully")
            except Exception as e:
                print("✗ Error: %s" % str(e))
        else:
            print("Error: File must be a .py file")
    else:
        # Directory
        print("Processing directory: %s" % args.path)
        processed_files = cleanup_directory(args.path, backup, preserve_docstrings, preserve_shebang)
        print("\nCompleted! Processed %d files." % len(processed_files))

if __name__ == "__main__":
    main()