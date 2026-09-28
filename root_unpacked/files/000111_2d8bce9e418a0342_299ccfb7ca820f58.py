#!/usr/bin/env python
# -*- coding: windows-1250 -*-

import os
import sys
import re
from collections import defaultdict

def collect_strings_from_python_files():
    """Collect all strings from *.py files in root/ and uiscript/"""
    found_strings = set()
    
    # Patterns to match string literals
    string_patterns = [
        r'"([^"]+)"',  # Double quoted strings
        r"'([^']+)'",  # Single quoted strings
    ]
    
    directories = ['root', 'uiscript']
    
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            continue
            
        print(f"Scanning {directory}/ for strings...")
        
        for root_dir, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root_dir, file)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            for pattern in string_patterns:
                                matches = re.findall(pattern, content)
                                for match in matches:
                                    # Filter out system/path strings and very short strings
                                    clean_match = match.strip()
                                    if (len(clean_match) > 2 and 
                                        not clean_match.startswith('/') and 
                                        not clean_match.startswith('\\') and
                                        not clean_match.startswith('http') and
                                        not clean_match.startswith('www') and
                                        not clean_match.endswith('.py') and
                                        not clean_match.endswith('.txt') and
                                        not clean_match.endswith('.log') and
                                        not re.match(r'^[0-9.]+$', clean_match) and
                                        not re.match(r'^[a-z_]+$', clean_match.lower())):
                                        found_strings.add(clean_match)
                    
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
    
    print(f"Found {len(found_strings)} potential translation strings")
    return found_strings

def load_all_locale_keys():
    """Load all keys from all locale files"""
    all_keys = set()
    
    languages = ['cz', 'de', 'en', 'pl']
    locale_files = [
        'locale_game.txt',
        'locale_game_new.txt', 
        'locale_interface.txt',
        'locale_interface_new.txt'
    ]
    
    for lang in languages:
        lang_dir = f"locale/{lang}"
        if not os.path.exists(lang_dir):
            continue
        
        for locale_file in locale_files:
            file_path = os.path.join(lang_dir, locale_file)
            
            if not os.path.exists(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='windows-1250', errors='ignore') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = line.split('\t', 1)
                            if parts:
                                key = parts[0].strip()
                                if key:
                                    all_keys.add(key)
            
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    print(f"Found {len(all_keys)} keys in locale files")
    return all_keys

def extract_missing_locales():
    """Extract strings that are in Python files but missing from locale files"""
    print("Missing Locales Extraction Tool")
    print("=" * 50)
    
    # Get strings from Python files
    python_strings = collect_strings_from_python_files()
    
    # Get all keys from locale files
    locale_keys = load_all_locale_keys()
    
    # Find missing translations
    missing_locales = python_strings - locale_keys
    
    print(f"\n" + "=" * 50)
    print(f"MISSING LOCALE KEYS: {len(missing_locales)}")
    print("=" * 50)
    
    if missing_locales:
        # Sort by length and alphabetically for better readability
        sorted_missing = sorted(missing_locales, key=lambda x: (len(x), x.lower()))
        
        # Write to file
        output_file = "missing_locales.txt"
        with open(output_file, 'w', encoding='windows-1250') as f:
            f.write("# Missing locale keys found in Python files\n")
            f.write("# Format: KEY[TAB]TRANSLATION\n")
            f.write("# Add translations and copy to appropriate locale files\n\n")
            
            for key in sorted_missing:
                f.write(f"{key}\t\n")
        
        print(f"Missing keys saved to: {output_file}")
        print(f"\nFirst 20 missing keys:")
        
        for i, key in enumerate(sorted_missing[:20]):
            print(f"  {i+1:2d}. {key}")
        
        if len(missing_locales) > 20:
            print(f"  ... and {len(missing_locales) - 20} more (see {output_file})")
        
        # Also create template files for each language
        languages = ['cz', 'de', 'en', 'pl']
        for lang in languages:
            template_file = f"missing_locales_{lang}.txt"
            with open(template_file, 'w', encoding='windows-1250') as f:
                f.write(f"# Missing locale keys for {lang.upper()}\n")
                f.write("# Add translations and append to appropriate locale files\n\n")
                
                for key in sorted_missing:
                    f.write(f"{key}\t\n")
            
            print(f"Template created: {template_file}")
    
    else:
        print("No missing locale keys found!")
    
    # Statistics
    print(f"\n" + "=" * 50)
    print("STATISTICS:")
    print("=" * 50)
    print(f"Python strings found: {len(python_strings)}")
    print(f"Locale keys found: {len(locale_keys)}")
    print(f"Missing translations: {len(missing_locales)}")
    print(f"Coverage: {((len(locale_keys) / len(python_strings)) * 100):.1f}%" if python_strings else "N/A")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--strings-only':
            # Just show Python strings
            strings = collect_strings_from_python_files()
            print(f"\nAll strings from Python files ({len(strings)}):")
            for string in sorted(strings):
                print(f"  {string}")
        elif sys.argv[1] == '--keys-only':
            # Just show locale keys
            keys = load_all_locale_keys()
            print(f"\nAll keys from locale files ({len(keys)}):")
            for key in sorted(keys):
                print(f"  {key}")
        else:
            print("Usage:")
            print("  python extract_missing_locales.py           # Extract missing locales")
            print("  python extract_missing_locales.py --strings-only  # Show Python strings")
            print("  python extract_missing_locales.py --keys-only     # Show locale keys")
    else:
        extract_missing_locales()

if __name__ == "__main__":
    main()