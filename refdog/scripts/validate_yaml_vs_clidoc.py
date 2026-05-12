#!/usr/bin/env python3
"""
Validate current YAML command configs against cli-doc files.

This shows what would change if we switched to cli-doc as the source of truth.
"""

import os
import sys
import yaml
import re
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

def parse_cli_doc_file(file_path):
    """Parse a cli-doc markdown file (simplified version)."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    result = {
        'name': '',
        'synopsis': '',
        'options': []
    }
    
    # Extract command name from title
    for line in lines:
        if line.startswith('## '):
            result['name'] = line[3:].strip()
            break
    
    # Extract synopsis
    in_synopsis = False
    synopsis_lines = []
    for line in lines:
        if line.strip() == '### Synopsis':
            in_synopsis = True
            continue
        if in_synopsis:
            if line.startswith('###') or line.startswith('```'):
                break
            if line.strip():
                synopsis_lines.append(line.strip())
    result['synopsis'] = ' '.join(synopsis_lines)
    
    # Extract options
    in_options = False
    for line in lines:
        if line.strip() == '### Options':
            in_options = True
            continue
        
        if in_options:
            if line.startswith('###'):
                break
            
            if line.strip().startswith('-'):
                # Parse option line
                match = re.match(r'\s*(-\w+)?,?\s*(--[\w-]+)?\s+(\w+)?\s*(.*)', line)
                if match:
                    short, long, opt_type, desc = match.groups()
                    name = long.strip() if long else short.strip()
                    name = name.lstrip('-')
                    
                    # Infer type
                    if opt_type and opt_type[0].islower() and desc and desc[0].islower():
                        inferred_type = 'bool'
                    elif opt_type:
                        inferred_type = opt_type.lower()
                    else:
                        inferred_type = 'bool'
                    
                    result['options'].append({
                        'name': name,
                        'type': inferred_type
                    })
    
    return result

def load_yaml_commands(config_dir):
    """Load all YAML command configs."""
    commands = {}
    
    for yaml_file in os.listdir(config_dir):
        if yaml_file.endswith('.yaml') and yaml_file not in ['options.yaml', 'groups.yaml']:
            path = os.path.join(config_dir, yaml_file)
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
                if data and 'name' in data:
                    commands[data['name']] = data
    
    return commands

def find_cli_doc_file(cli_doc_dir, command_name):
    """Find the cli-doc file for a command."""
    parts = command_name.split()
    filename = 'skupper_' + '_'.join(parts) + '.md'
    path = os.path.join(cli_doc_dir, filename)
    
    if os.path.exists(path):
        return path
    
    return None

def compare_command(yaml_data, cli_doc_data, command_name):
    """Compare YAML config with cli-doc data."""
    issues = []
    
    # Compare description/synopsis
    yaml_desc = yaml_data.get('description', '').strip()
    cli_synopsis = cli_doc_data.get('synopsis', '').strip()
    
    if yaml_desc and cli_synopsis:
        # Just note if they're different (not necessarily wrong)
        if yaml_desc.lower() != cli_synopsis.lower():
            issues.append({
                'type': 'description_diff',
                'severity': 'info',
                'message': 'Description differs from cli-doc synopsis'
            })
    
    # Compare options (for subcommands)
    if 'subcommands' in yaml_data:
        for subcmd in yaml_data['subcommands']:
            subcmd_name = f"{command_name} {subcmd['name']}"
            cli_doc_path = find_cli_doc_file(os.path.dirname(os.path.dirname(__file__)) + '/cli-doc', subcmd_name)
            
            if cli_doc_path:
                subcmd_cli_doc = parse_cli_doc_file(cli_doc_path)
                subcmd_issues = compare_options(subcmd, subcmd_cli_doc, subcmd_name)
                issues.extend(subcmd_issues)
    
    return issues

def compare_options(yaml_cmd, cli_doc_data, command_name):
    """Compare options between YAML and cli-doc."""
    issues = []
    
    # Get YAML options
    yaml_options = yaml_cmd.get('options', [])
    yaml_opt_names = {opt['name'] for opt in yaml_options if isinstance(opt, dict) and 'name' in opt}
    
    # Get cli-doc options
    cli_doc_options = cli_doc_data.get('options', [])
    cli_doc_opt_names = {opt['name'] for opt in cli_doc_options}
    
    # Check for options in YAML not in cli-doc
    extra_in_yaml = yaml_opt_names - cli_doc_opt_names
    if extra_in_yaml:
        for opt_name in extra_in_yaml:
            issues.append({
                'type': 'extra_option',
                'severity': 'warning',
                'command': command_name,
                'option': opt_name,
                'message': f"Option '{opt_name}' defined in YAML but not in cli-doc"
            })
    
    # Check for options in cli-doc not in YAML
    missing_in_yaml = cli_doc_opt_names - yaml_opt_names
    if missing_in_yaml:
        for opt_name in missing_in_yaml:
            issues.append({
                'type': 'missing_option',
                'severity': 'info',
                'command': command_name,
                'option': opt_name,
                'message': f"Option '{opt_name}' in cli-doc but not explicitly defined in YAML"
            })
    
    return issues

def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    cli_doc_dir = repo_root / "cli-doc"
    config_dir = repo_root / "config" / "commands"
    
    if not cli_doc_dir.exists():
        print(f"❌ cli-doc directory not found: {cli_doc_dir}")
        return 1
    
    if not config_dir.exists():
        print(f"❌ Config directory not found: {config_dir}")
        return 1
    
    print("🔍 Validating YAML configs against cli-doc files...\n")
    
    # Load YAML commands
    yaml_commands = load_yaml_commands(config_dir)
    print(f"📋 Loaded {len(yaml_commands)} YAML command configs\n")
    
    all_issues = []
    commands_checked = 0
    
    # Check each YAML command
    for cmd_name, yaml_data in sorted(yaml_commands.items()):
        # Find corresponding cli-doc
        cli_doc_path = find_cli_doc_file(cli_doc_dir, cmd_name)
        
        if not cli_doc_path:
            print(f"⚠️  {cmd_name}: No cli-doc file found")
            continue
        
        # Parse cli-doc
        try:
            cli_doc_data = parse_cli_doc_file(cli_doc_path)
        except Exception as e:
            print(f"❌ {cmd_name}: Error parsing cli-doc: {e}")
            continue
        
        commands_checked += 1
        
        # Compare
        issues = compare_command(yaml_data, cli_doc_data, cmd_name)
        
        if issues:
            all_issues.extend(issues)
            print(f"⚠️  {cmd_name}: {len(issues)} issues")
            for issue in issues:
                if issue['severity'] == 'warning':
                    print(f"    ⚠️  {issue['message']}")
                else:
                    print(f"    ℹ️  {issue['message']}")
        else:
            print(f"✅ {cmd_name}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 Validation Summary")
    print("="*60)
    print(f"Commands checked: {commands_checked}")
    print(f"Total issues: {len(all_issues)}")
    
    warnings = [i for i in all_issues if i['severity'] == 'warning']
    infos = [i for i in all_issues if i['severity'] == 'info']
    
    print(f"Warnings: {len(warnings)}")
    print(f"Info: {len(infos)}")
    
    if warnings:
        print("\n⚠️  Warnings indicate potential problems")
    if infos:
        print("ℹ️  Info items are for awareness (may be intentional)")
    
    if len(all_issues) == 0:
        print("\n✅ All validations passed!")
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())

# Made with Bob
