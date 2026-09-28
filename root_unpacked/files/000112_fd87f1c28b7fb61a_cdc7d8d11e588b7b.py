#!/usr/bin/env python
# -*- coding: windows-1250 -*-

import os
import sys
from collections import defaultdict

def load_locale_file(file_path):
    """Load a locale file and return dictionary of key-value pairs"""
    translations = {}
    
    if not os.path.exists(file_path):
        return translations
    
    try:
        with open(file_path, 'r', encoding='windows-1250', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('\t', 1)
                    if len(parts) >= 1:
                        key = parts[0].strip()
                        translation = parts[1].strip() if len(parts) > 1 else ""
                        if key:
                            translations[key] = translation
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return translations

def extract_missing_translations():
    """Extract translations missing in other languages compared to Czech"""
    print("Missing Translations Extractor (Czech as reference)")
    print("=" * 60)
    
    languages = ['cz', 'de', 'en', 'pl']
    locale_files = [
        'locale_game.txt',
        'locale_game_new.txt', 
        'locale_interface.txt',
        'locale_interface_new.txt'
    ]
    
    # Load Czech translations (reference)
    czech_translations = {}
    czech_dir = "locale/cz"
    
    if not os.path.exists(czech_dir):
        print(f"Czech locale directory not found: {czech_dir}")
        return
    
    print("Loading Czech translations (reference)...")
    for locale_file in locale_files:
        file_path = os.path.join(czech_dir, locale_file)
        translations = load_locale_file(file_path)
        czech_translations[locale_file] = translations
        print(f"  {locale_file}: {len(translations)} keys")
    
    # Get all Czech keys
    all_czech_keys = set()
    for translations in czech_translations.values():
        all_czech_keys.update(translations.keys())
    
    print(f"\nTotal Czech keys: {len(all_czech_keys)}")
    
    # Compare with other languages
    for lang in languages:
        if lang == 'cz':
            continue
            
        print(f"\n" + "=" * 60)
        print(f"MISSING TRANSLATIONS FOR {lang.upper()}")
        print("=" * 60)
        
        lang_dir = f"locale/{lang}"
        if not os.path.exists(lang_dir):
            print(f"Directory not found: {lang_dir}")
            continue
        
        # Load translations for this language
        lang_translations = {}
        for locale_file in locale_files:
            file_path = os.path.join(lang_dir, locale_file)
            translations = load_locale_file(file_path)
            lang_translations[locale_file] = translations
        
        # Find missing keys per file
        for locale_file in locale_files:
            czech_keys = set(czech_translations[locale_file].keys())
            lang_keys = set(lang_translations[locale_file].keys())
            missing_keys = czech_keys - lang_keys
            
            if missing_keys:
                print(f"\n{locale_file}: {len(missing_keys)} missing translations")
                print("-" * 40)
                
                # Create output file
                output_file = f"missing_{lang}_{locale_file}"
                with open(output_file, 'w', encoding='windows-1250') as f:
                    f.write(f"# Missing translations for {lang.upper()} in {locale_file}\n")
                    f.write(f"# Czech -> {lang.upper()}\n")
                    f.write("# Format: KEY[TAB]TRANSLATION\n\n")
                    
                    # Sort missing keys
                    for key in sorted(missing_keys):
                        czech_text = czech_translations[locale_file].get(key, "")
                        f.write(f"{key}\t{czech_text}\n")
                
                print(f"Created: {output_file}")
                
                # Show first few missing keys
                print("First 10 missing keys:")
                for i, key in enumerate(sorted(list(missing_keys)[:10])):
                    czech_text = czech_translations[locale_file].get(key, "")
                    print(f"  {key} -> {czech_text}")
            else:
                print(f"\n{locale_file}: No missing translations!")
        
        # Summary for this language
        total_lang_keys = sum(len(translations) for translations in lang_translations.values())
        total_czech_keys = sum(len(translations) for translations in czech_translations.values())
        missing_total = total_czech_keys - total_lang_keys
        
        print(f"\nSUMMARY FOR {lang.upper()}:")
        print(f"Czech total keys: {total_czech_keys}")
        print(f"{lang.upper()} total keys: {total_lang_keys}")
        print(f"Missing translations: {missing_total}")
        print(f"Coverage: {((total_lang_keys / total_czech_keys) * 100):.1f}%" if total_czech_keys > 0 else "N/A")

def main():
    """Main function"""
    extract_missing_translations()

if __name__ == "__main__":
    main()