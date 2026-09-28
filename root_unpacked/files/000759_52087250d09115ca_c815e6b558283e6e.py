#!/usr/bin/env python
# -*- coding: windows-1250 -*-

import os
import sys
import re
from collections import OrderedDict

def natural_sort_key(text):
    """
    Natural sorting key function that handles numeric parts properly
    DETAILS_7, DETAILS_8, DETAILS_70 instead of DETAILS_70, DETAILS_7, DETAILS_8
    """
    def convert(text):
        return int(text) if text.isdigit() else text.lower()
    
    return [convert(c) for c in re.split('([0-9]+)', text)]

def process_locale_file(file_path):
    """Process a single locale file - remove duplicates and sort"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    
    print(f"Processing: {file_path}")
    
    # Read the file
    translations = OrderedDict()
    comments = []
    
    try:
        with open(file_path, 'r', encoding='windows-1250', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                original_line = line.rstrip('\r\n')
                
                # Keep comments at the top
                if original_line.startswith('#') or not original_line.strip():
                    if not translations:  # Only keep comments at the beginning
                        comments.append(original_line)
                    continue
                
                # Parse key-value pairs
                parts = original_line.split('\t', 1)
                if len(parts) >= 2:
                    key = parts[0].strip()
                    translation = parts[1].strip()
                    
                    if key in translations:
                        print(f"  Duplicate found: {key} (line {line_num})")
                    
                    translations[key] = translation
                elif len(parts) == 1 and parts[0].strip():
                    key = parts[0].strip()
                    if key in translations:
                        print(f"  Duplicate found: {key} (line {line_num})")
                    translations[key] = ""
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
    # Sort translations by key using natural sorting
    sorted_translations = OrderedDict(sorted(translations.items(), key=lambda x: natural_sort_key(x[0])))
    
    # Write back to file
    try:
        with open(file_path, 'w', encoding='windows-1250') as f:
            # Write comments first
            for comment in comments:
                f.write(comment + '\n')
            
            if comments:
                f.write('\n')  # Empty line after comments
            
            # Write sorted translations
            for key, translation in sorted_translations.items():
                if translation:
                    f.write(f"{key}\t{translation}\n")
                else:
                    f.write(f"{key}\n")
    
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False
    
    original_count = len(translations)
    final_count = len(sorted_translations)
    duplicates_removed = original_count - final_count if original_count != final_count else 0
    
    print(f"  Keys: {final_count}, Duplicates removed: {duplicates_removed}")
    return True

def main():
    """Main function to process all locale files"""
    languages = ['cz', 'de', 'en', 'pl']
    locale_files = [
        'locale_game.txt',
        'locale_game_new.txt', 
        'locale_interface.txt',
        'locale_interface_new.txt'
    ]
    
    print("Locale Files Sorter and Duplicate Cleaner")
    print("=" * 50)
    
    total_processed = 0
    total_errors = 0
    
    for lang in languages:
        print(f"\nProcessing language: {lang.upper()}")
        print("-" * 30)
        
        lang_dir = f"locale/{lang}"
        if not os.path.exists(lang_dir):
            print(f"Directory not found: {lang_dir}")
            continue
        
        for locale_file in locale_files:
            file_path = os.path.join(lang_dir, locale_file)
            
            if process_locale_file(file_path):
                total_processed += 1
            else:
                total_errors += 1
    
    print(f"\n" + "=" * 50)
    print(f"Summary:")
    print(f"Files processed successfully: {total_processed}")
    print(f"Files with errors: {total_errors}")
    print(f"Total files: {total_processed + total_errors}")

if __name__ == "__main__":
    main()