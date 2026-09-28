#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from collections import OrderedDict

def read_locale_file(filepath):
    """Read locale file and return dictionary of key-value pairs"""
    locale_dict = OrderedDict()
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return locale_dict
    
    # Try different encodings
    encodings = ['utf-8', 'windows-1250', 'iso-8859-2', 'cp1252', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and '\t' in line:
                        parts = line.split('\t', 1)
                        if len(parts) == 2:
                            key, value = parts
                            locale_dict[key] = value
                        else:
                            print(f"Warning: Invalid format in {filepath} line {line_num}: {line}")
            print(f"Successfully read {filepath} with {encoding} encoding")
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading {filepath} with {encoding}: {e}")
            continue
    
    if not locale_dict:
        print(f"Could not read {filepath} with any encoding")
    
    return locale_dict

def write_locale_file(filepath, locale_dict, encoding='windows-1250'):
    """Write dictionary to locale file in proper format"""
    try:
        with open(filepath, 'w', encoding=encoding) as f:
            for key, value in locale_dict.items():
                f.write(f"{key}\t{value}\n")
        print(f"Successfully wrote {len(locale_dict)} entries to {filepath}")
    except Exception as e:
        print(f"Error writing {filepath}: {e}")

def compare_and_sync_locales():
    """Compare Czech and Polish locale files and synchronize them"""
    
    locale_files = [
        'locale_game.txt',
        'locale_game_new.txt', 
        'locale_interface.txt',
        'locale_interface_new.txt'
    ]
    
    base_path = 'locale'
    cz_path = os.path.join(base_path, 'cz')
    pl_path = os.path.join(base_path, 'pl')
    
    for filename in locale_files:
        print(f"\n=== Processing {filename} ===")
        
        cz_file = os.path.join(cz_path, filename)
        pl_file = os.path.join(pl_path, filename)
        
        # Read both files
        cz_dict = read_locale_file(cz_file)
        pl_dict = read_locale_file(pl_file)
        
        print(f"Czech entries: {len(cz_dict)}")
        print(f"Polish entries: {len(pl_dict)}")
        
        # Find missing keys
        cz_keys = set(cz_dict.keys())
        pl_keys = set(pl_dict.keys())
        
        missing_in_pl = cz_keys - pl_keys
        missing_in_cz = pl_keys - cz_keys
        
        if missing_in_pl:
            print(f"Missing in Polish ({len(missing_in_pl)} keys):")
            for key in sorted(missing_in_pl):
                print(f"  {key}")
                # Add to Polish with Czech value as placeholder
                pl_dict[key] = f"[PL_MISSING] {cz_dict[key]}"
        
        if missing_in_cz:
            print(f"Missing in Czech ({len(missing_in_cz)} keys):")
            for key in sorted(missing_in_cz):
                print(f"  {key}")
                # Add to Czech with Polish value as placeholder
                cz_dict[key] = f"[CZ_MISSING] {pl_dict[key]}"
        
        # Sort dictionaries by key for consistency
        cz_sorted = OrderedDict(sorted(cz_dict.items()))
        pl_sorted = OrderedDict(sorted(pl_dict.items()))
        
        # Write synchronized files
        if missing_in_pl or missing_in_cz:
            backup_cz = cz_file + '.backup'
            backup_pl = pl_file + '.backup'
            
            # Create backups
            if os.path.exists(cz_file):
                os.rename(cz_file, backup_cz)
                print(f"Backup created: {backup_cz}")
            
            if os.path.exists(pl_file):
                os.rename(pl_file, backup_pl)
                print(f"Backup created: {backup_pl}")
            
            # Write synchronized files
            write_locale_file(cz_file, cz_sorted)
            write_locale_file(pl_file, pl_sorted)
            
            print(f"Synchronized! Both files now have {len(cz_sorted)} entries")
        else:
            print("Files are already synchronized!")

def main():
    print("Locale Synchronization Script")
    print("=============================")
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    if not os.path.exists('locale'):
        print("Error: 'locale' directory not found!")
        sys.exit(1)
    
    compare_and_sync_locales()
    print("\nSynchronization complete!")

if __name__ == "__main__":
    main()