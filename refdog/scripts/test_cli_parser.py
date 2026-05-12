#!/usr/bin/env python3
"""Test the CLI parser without importing common"""

import sys
import os
import re

# Minimal functions needed
def read(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def list_dir(path):
    return os.listdir(path)

def join(*args):
    return os.path.join(*args)

def debug(msg):
    print(f"DEBUG: {msg}")

def warning(msg):
    print(f"WARNING: {msg}")

# Include the parser functions inline
def parse_cli_doc(filepath):
    """Parse a cli-doc markdown file"""
    content = read(filepath)
    
    command_info = {
        "name": extract_command_name(content),
        "title": extract_title(content),
        "synopsis": extract_synopsis(content),
        "usage": extract_usage(content),
        "options": extract_options(content, "### Options"),
        "inherited_options": extract_options(content, "### Options inherited from parent commands"),
        "examples": extract_examples(content),
        "see_also": extract_see_also(content),
    }
    
    return command_info

def extract_command_name(content):
    lines = content.split('\n')
    for line in lines:
        if line.startswith('## skupper '):
            return line[11:].strip()
    return None

def extract_title(content):
    lines = content.split('\n')
    for line in lines:
        if line.startswith('## skupper '):
            return line[3:].strip()
    return None

def extract_synopsis(content):
    lines = content.split('\n')
    synopsis_lines = []
    in_synopsis = False
    
    for line in lines:
        if line.startswith('### Synopsis'):
            in_synopsis = True
            continue
        if in_synopsis:
            if line.startswith('```') or line.startswith('###'):
                break
            if line.strip():
                synopsis_lines.append(line)
    
    return '\n'.join(synopsis_lines).strip()

def extract_usage(content):
    lines = content.split('\n')
    in_synopsis = False
    in_code_block = False
    usage_lines = []
    
    for line in lines:
        if line.startswith('### Synopsis'):
            in_synopsis = True
            continue
        if in_synopsis and line.strip() == '```':
            if not in_code_block:
                in_code_block = True
                continue
            else:
                break
        if in_code_block:
            usage_lines.append(line)
    
    return '\n'.join(usage_lines).strip()

def extract_options(content, section_header):
    lines = content.split('\n')
    options = []
    in_section = False
    current_option = None
    
    for line in lines:
        if line.startswith(section_header):
            in_section = True
            continue
        
        if in_section and line.startswith('###'):
            break
        
        if not in_section:
            continue
        
        if line.strip().startswith('--') or line.strip().startswith('-h,'):
            if current_option:
                options.append(current_option)
            current_option = parse_option_line(line)
        elif current_option and line.strip():
            if 'description' in current_option:
                current_option['description'] += ' ' + line.strip()
            else:
                current_option['description'] = line.strip()
    
    if current_option:
        options.append(current_option)
    
    for option in options:
        post_process_option(option)
    
    return options

def parse_option_line(line):
    option = {}
    line = line.strip()
    parts = re.split(r'\s{2,}', line, maxsplit=1)
    
    if len(parts) < 1:
        return option
    
    flag_part = parts[0]
    desc_part = parts[1] if len(parts) > 1 else ""
    
    if ', --' in flag_part:
        long_flag = flag_part.split(', --')[1].split()[0]
        option['name'] = long_flag
    elif flag_part.startswith('--'):
        flag_parts = flag_part.split()
        option['name'] = flag_parts[0][2:]
        if len(flag_parts) > 1:
            option['type'] = flag_parts[1]
    elif flag_part.startswith('-'):
        option['name'] = flag_part[1:]
    
    if desc_part:
        option['description'] = desc_part
    
    return option

def post_process_option(option):
    if 'description' not in option:
        return
    
    desc = option['description']
    
    default_match = re.search(r'\(default[:\s]+([^)]+)\)', desc)
    if default_match:
        option['default'] = default_match.group(1).strip()
    
    choices_match = re.search(r'Choices:\s*\[([^\]]+)\]', desc)
    if choices_match:
        choices_str = choices_match.group(1)
        option['choices'] = [c.strip() for c in choices_str.split('|')]
    
    if 'type' not in option:
        if 'duration' in desc.lower() or option.get('default', '').endswith(('s', 'm')):
            option['type'] = 'duration'
        elif option.get('default') in ['true', 'false']:
            option['type'] = 'boolean'
        elif 'choices' in option:
            option['type'] = 'string'

def extract_examples(content):
    lines = content.split('\n')
    examples = []
    in_examples = False
    in_code_block = False
    current_example = []
    
    for line in lines:
        if line.startswith('### Examples'):
            in_examples = True
            continue
        
        if in_examples and line.startswith('###'):
            break
        
        if not in_examples:
            continue
        
        if line.strip() == '```':
            if not in_code_block:
                in_code_block = True
                current_example = []
            else:
                in_code_block = False
                if current_example:
                    examples.append('\n'.join(current_example).strip())
            continue
        
        if in_code_block:
            current_example.append(line)
    
    return examples

def extract_see_also(content):
    lines = content.split('\n')
    see_also = []
    in_section = False
    
    for line in lines:
        if line.startswith('### SEE ALSO'):
            in_section = True
            continue
        
        if in_section and line.startswith('#'):
            break
        
        if not in_section:
            continue
        
        link_match = re.match(r'\*\s+\[([^\]]+)\]\(([^)]+)\)', line.strip())
        if link_match:
            see_also.append({
                'title': link_match.group(1),
                'href': link_match.group(2),
            })
    
    return see_also

# Main test
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != '--all':
        filepath = sys.argv[1]
        info = parse_cli_doc(filepath)
        
        print(f"Command: {info['name']}")
        print(f"Title: {info['title']}")
        print(f"\nSynopsis:\n{info['synopsis']}")
        print(f"\nUsage:\n{info['usage']}")
        print(f"\nOptions ({len(info['options'])}):")
        for opt in info['options']:
            print(f"  --{opt['name']}")
            print(f"    Type: {opt.get('type', 'N/A')}")
            print(f"    Default: {opt.get('default', 'N/A')}")
            print(f"    Desc: {opt.get('description', '')[:80]}...")
            if 'choices' in opt:
                print(f"    Choices: {opt['choices']}")
        print(f"\nInherited Options ({len(info['inherited_options'])}):")
        for opt in info['inherited_options']:
            print(f"  --{opt['name']}: {opt.get('description', '')[:60]}...")
        print(f"\nExamples ({len(info['examples'])}):")
        for ex in info['examples']:
            print(f"  {ex[:80]}...")
        print(f"\nSee Also ({len(info['see_also'])}):")
        for sa in info['see_also']:
            print(f"  {sa['title']} -> {sa['href']}")
    elif len(sys.argv) > 1 and sys.argv[1] == '--all':
        # Parse all cli-doc files
        cli_doc_dir = "cli-doc"
        commands = {}
        errors = []
        
        for filename in sorted(os.listdir(cli_doc_dir)):
            if not filename.endswith('.md'):
                continue
            
            filepath = os.path.join(cli_doc_dir, filename)
            try:
                info = parse_cli_doc(filepath)
                if info['name']:
                    commands[info['name']] = info
                    print(f"✓ {filename:40s} -> {info['name']}")
                else:
                    errors.append(f"✗ {filename}: No command name found")
            except Exception as e:
                errors.append(f"✗ {filename}: {e}")
        
        print(f"\n{'='*70}")
        print(f"Parsed {len(commands)} commands successfully")
        if errors:
            print(f"\nErrors ({len(errors)}):")
            for err in errors:
                print(f"  {err}")
    else:
        print("Usage:")
        print("  python test_cli_parser.py <cli-doc-file>  # Parse single file")
        print("  python test_cli_parser.py --all           # Parse all files")
        print("\nExample:")
        print("  python test_cli_parser.py cli-doc/skupper_site_create.md")

# Made with Bob
