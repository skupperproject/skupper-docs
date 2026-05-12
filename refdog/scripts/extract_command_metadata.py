#!/usr/bin/env python3
"""
Extract metadata from existing command YAML config files.
Creates minimal metadata files that supplement cli-doc information.
"""

import os
import sys

# Add python directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python"))

try:
    from plano import read_yaml, emit_yaml, list_dir, join, notice, warning
except ImportError:
    print("ERROR: Could not import plano. Make sure you're in the right directory.")
    sys.exit(1)

def extract_command_metadata(yaml_config_path, output_dir):
    """Extract metadata from a command YAML config file"""
    notice(f"Processing {yaml_config_path}")
    
    data = read_yaml(yaml_config_path)
    command_name = data.get('name')
    
    if not command_name:
        warning(f"No command name in {yaml_config_path}")
        return 0
    
    # Process each subcommand
    count = 0
    for subcommand in data.get('subcommands', []):
        subcommand_name = subcommand.get('name')
        if not subcommand_name:
            continue
        
        full_command = f"{command_name} {subcommand_name}"
        
        metadata = {
            "command": full_command,
        }
        
        # Enhanced examples (not basic ones from cli-doc)
        if 'examples' in subcommand and subcommand['examples']:
            metadata["examples"] = parse_examples(subcommand['examples'])
        
        # Cross-references
        if 'related_commands' in subcommand:
            metadata["related_commands"] = subcommand['related_commands']
        
        if 'related_resources' in data:
            metadata["related_resources"] = data['related_resources']
        elif 'resource' in data:
            metadata["related_resources"] = [data['resource']]
        
        if 'related_concepts' in subcommand:
            metadata["related_concepts"] = subcommand['related_concepts']
        
        # Links
        if 'links' in subcommand:
            metadata["links"] = subcommand['links']
        
        # Error documentation
        if 'errors' in subcommand:
            metadata["errors"] = subcommand['errors']
        
        # Wait conditions
        if 'wait' in subcommand:
            metadata["wait"] = {
                "default": subcommand['wait'],
                "description": f"Waits for {subcommand['wait']} status by default"
            }
        
        # Option metadata (grouping, additional notes)
        if 'options' in subcommand:
            option_metadata = {}
            for opt in subcommand['options']:
                opt_name = opt.get('name')
                if not opt_name:
                    continue
                
                opt_meta = {}
                
                if 'group' in opt:
                    opt_meta['group'] = opt['group']
                
                if 'related_concepts' in opt:
                    opt_meta['related_concepts'] = opt['related_concepts']
                
                if 'related_resources' in opt:
                    opt_meta['related_resources'] = opt['related_resources']
                
                if 'links' in opt:
                    opt_meta['links'] = opt['links']
                
                # Add notes if description is different from cli-doc
                # (we'll manually review these later)
                if 'description' in opt and opt['description'].strip():
                    # Only add as note if it's substantial
                    desc = opt['description'].strip()
                    if len(desc) > 50:  # Arbitrary threshold
                        opt_meta['notes'] = desc
                
                if opt_meta:
                    option_metadata[opt_name] = opt_meta
            
            if option_metadata:
                metadata["options"] = option_metadata
        
        # Write metadata file
        output_filename = f"{command_name}-{subcommand_name}.yaml"
        output_path = join(output_dir, output_filename)
        
        emit_yaml(output_path, metadata)
        notice(f"  Created {output_filename}")
        count += 1
    
    return count

def parse_examples(examples_text):
    """
    Parse examples from text format to structured format.
    
    Input format:
      # Comment
      $ command
      output line 1
      output line 2
      
      # Another comment
      $ another command
    
    Output format:
      [
        {
          "description": "Comment",
          "command": "command",
          "output": "output line 1\noutput line 2"
        },
        ...
      ]
    """
    if not examples_text:
        return []
    
    examples = []
    lines = examples_text.strip().split('\n')
    
    current_example = None
    current_output = []
    
    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith('#'):
            # Save previous example if exists
            if current_example:
                if current_output:
                    current_example['output'] = '\n'.join(current_output).strip()
                examples.append(current_example)
            
            # Start new example
            current_example = {
                "description": stripped[1:].strip()
            }
            current_output = []
        
        elif stripped.startswith('$'):
            # Command line
            if current_example:
                current_example['command'] = stripped[1:].strip()
        
        elif stripped and current_example and 'command' in current_example:
            # Output line
            current_output.append(line.rstrip())
        
        elif not stripped and current_output:
            # Empty line in output
            current_output.append('')
    
    # Don't forget the last example
    if current_example:
        if current_output:
            current_example['output'] = '\n'.join(current_output).strip()
        examples.append(current_example)
    
    return examples

def main():
    """Extract metadata from all command YAML files"""
    config_dir = "config/commands"
    output_dir = "config/commands/metadata"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Skip these files
    skip_files = ["groups.yaml", "overview.md", "options.yaml"]
    
    total_commands = 0
    
    for filename in sorted(list_dir(config_dir)):
        if not filename.endswith(".yaml"):
            continue
        
        if filename in skip_files:
            continue
        
        input_path = join(config_dir, filename)
        
        # Skip if it's a directory
        if os.path.isdir(input_path):
            continue
        
        try:
            count = extract_command_metadata(input_path, output_dir)
            total_commands += count
        except Exception as e:
            warning(f"Failed to process {filename}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print(f"Metadata extraction complete!")
    print(f"Created metadata for {total_commands} commands")
    print(f"Files in {output_dir}")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Review extracted metadata files")
    print("2. Compare with cli-doc information")
    print("3. Remove redundant descriptions from metadata")
    print("4. Implement merge logic (Phase 3)")

if __name__ == "__main__":
    main()

# Made with Bob
