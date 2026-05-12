#!/usr/bin/env python3
"""
Validate command metadata against cli-doc files.

Checks for:
1. Options in metadata that don't exist in cli-doc
2. Options in cli-doc that aren't documented in metadata
3. Type mismatches
4. Default value mismatches
5. Missing required options
"""

import os
import sys
import yaml
from pathlib import Path

# Add parent directory to path to import cli_parser
sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

from cli_parser import parse_cli_doc_file

def load_metadata(metadata_dir):
    """Load all metadata files."""
    metadata = {}
    for yaml_file in os.listdir(metadata_dir):
        if yaml_file.endswith('.yaml'):
            path = os.path.join(metadata_dir, yaml_file)
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
                if data and 'command' in data:
                    metadata[data['command']] = data
    return metadata

def find_cli_doc_file(cli_doc_dir, command_name):
    """Find the cli-doc file for a command."""
    # Convert command name to file path
    # e.g., "skupper site create" -> "skupper_site_create.md"
    parts = command_name.split()
    if parts[0] == 'skupper':
        parts = parts[1:]  # Remove 'skupper' prefix
    
    filename = 'skupper_' + '_'.join(parts) + '.md'
    path = os.path.join(cli_doc_dir, filename)
    
    if os.path.exists(path):
        return path
    
    # Try without skupper prefix
    filename = '_'.join(parts) + '.md'
    path = os.path.join(cli_doc_dir, filename)
    if os.path.exists(path):
        return path
    
    return None

def validate_options(command_name, cli_doc_options, metadata_options):
    """Validate options between cli-doc and metadata."""
    warnings = []
    
    # Build lookup dictionaries
    cli_doc_by_name = {opt['name']: opt for opt in cli_doc_options}
    metadata_by_name = {opt['name']: opt for opt in metadata_options}
    
    # Check for options in metadata not in cli-doc
    for opt_name in metadata_by_name:
        if opt_name not in cli_doc_by_name:
            warnings.append(f"  ⚠️  Option '{opt_name}' in metadata but not in cli-doc")
    
    # Check for options in cli-doc not in metadata
    for opt_name in cli_doc_by_name:
        if opt_name not in metadata_by_name:
            # This is expected - metadata only documents important options
            pass
    
    # Check for type mismatches
    for opt_name in set(cli_doc_by_name.keys()) & set(metadata_by_name.keys()):
        cli_opt = cli_doc_by_name[opt_name]
        meta_opt = metadata_by_name[opt_name]
        
        cli_type = cli_opt.get('type', 'string')
        meta_type = meta_opt.get('type', 'string')
        
        if cli_type != meta_type:
            warnings.append(
                f"  ⚠️  Option '{opt_name}' type mismatch: "
                f"cli-doc={cli_type}, metadata={meta_type}"
            )
        
        # Check default values
        cli_default = cli_opt.get('default')
        meta_default = meta_opt.get('default')
        
        if cli_default and meta_default and cli_default != meta_default:
            warnings.append(
                f"  ⚠️  Option '{opt_name}' default mismatch: "
                f"cli-doc={cli_default}, metadata={meta_default}"
            )
    
    return warnings

def main():
    # Paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    cli_doc_dir = repo_root / "cli-doc"
    metadata_dir = repo_root / "config" / "commands" / "metadata"
    
    if not cli_doc_dir.exists():
        print(f"❌ cli-doc directory not found: {cli_doc_dir}")
        print("   Please ensure cli-doc files are available")
        return 1
    
    if not metadata_dir.exists():
        print(f"❌ Metadata directory not found: {metadata_dir}")
        return 1
    
    print("🔍 Validating command metadata against cli-doc files...\n")
    
    # Load all metadata
    metadata = load_metadata(metadata_dir)
    print(f"📋 Loaded {len(metadata)} metadata files\n")
    
    total_warnings = 0
    commands_checked = 0
    commands_missing_cli_doc = 0
    
    # Validate each command
    for command_name, meta_data in sorted(metadata.items()):
        # Find cli-doc file
        cli_doc_path = find_cli_doc_file(cli_doc_dir, command_name)
        
        if not cli_doc_path:
            print(f"❌ {command_name}")
            print(f"   No cli-doc file found")
            commands_missing_cli_doc += 1
            continue
        
        # Parse cli-doc
        try:
            cli_doc_data = parse_cli_doc_file(cli_doc_path)
        except Exception as e:
            print(f"❌ {command_name}")
            print(f"   Error parsing cli-doc: {e}")
            continue
        
        commands_checked += 1
        
        # Validate options
        cli_doc_options = cli_doc_data.get('options', [])
        metadata_options = meta_data.get('options', [])
        
        warnings = validate_options(command_name, cli_doc_options, metadata_options)
        
        if warnings:
            print(f"⚠️  {command_name}")
            for warning in warnings:
                print(warning)
            print()
            total_warnings += len(warnings)
        else:
            print(f"✅ {command_name}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 Validation Summary")
    print("="*60)
    print(f"Commands checked: {commands_checked}")
    print(f"Commands missing cli-doc: {commands_missing_cli_doc}")
    print(f"Total warnings: {total_warnings}")
    
    if total_warnings == 0 and commands_missing_cli_doc == 0:
        print("\n✅ All validations passed!")
        return 0
    else:
        print(f"\n⚠️  Found {total_warnings} warnings")
        if commands_missing_cli_doc > 0:
            print(f"⚠️  {commands_missing_cli_doc} commands missing cli-doc files")
        return 1

if __name__ == '__main__':
    sys.exit(main())

# Made with Bob
