#!/usr/bin/env python
# -*- coding: windows-1250 -*-

import os
import sys
import re
from collections import defaultdict, OrderedDict

def load_locale_file(file_path):
    """Load a locale file and return dictionary of key-value pairs"""
    translations = {}
    
    if not os.path.exists(file_path):
        return translations
    
    try:
        with open(file_path, 'r', encoding='windows-1250', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                original_line = line.rstrip('\r\n')
                
                # Skip comments and empty lines
                if original_line.startswith('#') or not original_line.strip():
                    continue
                
                # Parse key-value pairs
                parts = original_line.split('\t', 1)
                if len(parts) >= 1:
                    key = parts[0].strip()
                    translation = parts[1].strip() if len(parts) > 1 else ""
                    translations[key] = translation
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return translations

def collect_keys_from_python_files():
    """Collect all string keys from *.py files in root/ and uiscript/"""
    string_keys = set()
    
    # Patterns to match string literals
    string_patterns = [
        r'"([^"]*)"',  # Double quoted strings
        r"'([^']*)'",  # Single quoted strings
    ]
    
    directories = ['root', 'uiscript']
    
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            continue
            
        print(f"Scanning {directory}/ for Python files...")
        
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
                                    # Filter out obvious non-translation strings
                                    if len(match.strip()) > 0 and not match.startswith('/') and not match.startswith('\\'):
                                        string_keys.add(match.strip())
                    
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
    
    print(f"Found {len(string_keys)} unique strings in Python files")
    return string_keys

def compare_locale_files():
    """Compare locale files and find missing/unused keys"""
    languages = ['cz', 'de', 'en', 'pl']
    locale_files = [
        'locale_game.txt',
        'locale_game_new.txt', 
        'locale_interface.txt',
        'locale_interface_new.txt'
    ]
    
    print("Locale Files Comparison Tool")
    print("=" * 50)
    
    # Load all locale files
    all_locales = {}
    all_keys = set()
    
    for lang in languages:
        all_locales[lang] = {}
        lang_dir = f"locale/{lang}"
        
        if not os.path.exists(lang_dir):
            print(f"Directory not found: {lang_dir}")
            continue
        
        for locale_file in locale_files:
            file_path = os.path.join(lang_dir, locale_file)
            translations = load_locale_file(file_path)
            all_locales[lang][locale_file] = translations
            all_keys.update(translations.keys())
    
    print(f"Total unique keys found across all locale files: {len(all_keys)}")
    
    # Compare across languages
    print(f"\n" + "=" * 50)
    print("MISSING KEYS BY LANGUAGE:")
    print("=" * 50)
    
    for lang in languages:
        print(f"\nLanguage: {lang.upper()}")
        print("-" * 30)
        
        # Get all keys for this language
        lang_keys = set()
        for locale_file in locale_files:
            if locale_file in all_locales[lang]:
                lang_keys.update(all_locales[lang][locale_file].keys())
        
        missing_keys = all_keys - lang_keys
        
        if missing_keys:
            print(f"Missing {len(missing_keys)} keys:")
            for key in sorted(missing_keys):
                print(f"  - {key}")
        else:
            print("No missing keys!")
    
    # Compare files within same language
    print(f"\n" + "=" * 50)
    print("MISSING KEYS BETWEEN FILES (same language):")
    print("=" * 50)
    
    for lang in languages:
        if lang not in all_locales:
            continue
            
        print(f"\nLanguage: {lang.upper()}")
        print("-" * 30)
        
        # Get all keys for this language
        lang_all_keys = set()
        for locale_file in locale_files:
            if locale_file in all_locales[lang]:
                lang_all_keys.update(all_locales[lang][locale_file].keys())
        
        for locale_file in locale_files:
            if locale_file not in all_locales[lang]:
                continue
                
            file_keys = set(all_locales[lang][locale_file].keys())
            missing_in_file = lang_all_keys - file_keys
            
            if missing_in_file:
                print(f"  {locale_file} missing {len(missing_in_file)} keys:")
                for key in sorted(list(missing_in_file)[:10]):  # Show first 10
                    print(f"    - {key}")
                if len(missing_in_file) > 10:
                    print(f"    ... and {len(missing_in_file) - 10} more")
    
    # Collect strings from Python files and compare
    print(f"\n" + "=" * 50)
    print("PYTHON STRINGS vs LOCALE KEYS:")
    print("=" * 50)
    
    python_strings = collect_keys_from_python_files()
    
    # Find keys in locale files that are not used in Python
    unused_keys = all_keys - python_strings
    missing_translations = python_strings - all_keys
    
    print(f"\nUnused locale keys (in locale files but not in Python): {len(unused_keys)}")
    if unused_keys:
        print("First 20 unused keys:")
        for key in sorted(list(unused_keys)[:20]):
            print(f"  - {key}")
        if len(unused_keys) > 20:
            print(f"  ... and {len(unused_keys) - 20} more")
    
    print(f"\nMissing translations (in Python but not in locale files): {len(missing_translations)}")
    if missing_translations:
        print("First 20 missing translations:")
        for key in sorted(list(missing_translations)[:20]):
            print(f"  - {key}")
        if len(missing_translations) > 20:
            print(f"  ... and {len(missing_translations) - 20} more")
    
    # Statistics
    print(f"\n" + "=" * 50)
    print("STATISTICS:")
    print("=" * 50)
    
    for lang in languages:
        if lang not in all_locales:
            continue
            
        total_keys = 0
        for locale_file in locale_files:
            if locale_file in all_locales[lang]:
                file_key_count = len(all_locales[lang][locale_file])
                total_keys += file_key_count
                print(f"{lang}/{locale_file}: {file_key_count} keys")
        
        print(f"{lang} total: {total_keys} keys")
        print()

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--python-strings':
        # Just collect and show Python strings
        python_strings = collect_keys_from_python_files()
        print(f"\nAll strings found in Python files ({len(python_strings)}):")
        for string in sorted(python_strings):
            print(f"  {string}")
    else:
        # Full comparison
        compare_locale_files()

if __name__ == "__main__":
    main()