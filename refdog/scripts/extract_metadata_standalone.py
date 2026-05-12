#!/usr/bin/env python3
"""
Extract metadata from existing YAML config files to create minimal metadata files.
Standalone version - no dependencies on plano.
"""

import json
import os
import sys

def read_yaml_simple(filepath):
    """Simple YAML reader for our specific use case"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Use json for simple parsing (YAML is a superset of JSON for our files)
    # For more complex YAML, we'd need PyYAML, but let's try without first
    try:
        import yaml
        return yaml.safe_load(content)
    except ImportError:
        # Fallback: try to parse as JSON-like YAML
        print(f"Warning: PyYAML not available, using limited parser")
        # This won't work for complex YAML, but let's document the structure
        return None

def write_yaml_simple(filepath, data):
    """Simple YAML writer"""
    try:
        import yaml
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    except ImportError:
        # Fallback to JSON
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Warning: Wrote {filepath} as JSON (install PyYAML for proper YAML)")

def extract_metadata(yaml_config_path, output_path):
    """Extract non-CRD data from existing YAML config"""
    print(f"Extracting metadata from {yaml_config_path}")
    
    data = read_yaml_simple(yaml_config_path)
    
    if data is None:
        print(f"ERROR: Could not parse {yaml_config_path}")
        return None
    
    metadata = {
        "name": data.get("name"),
    }
    
    # Add optional top-level fields
    if "examples" in data:
        metadata["examples"] = data["examples"]
    
    if "related_resources" in data:
        metadata["related_resources"] = data["related_resources"]
    
    if "related_concepts" in data:
        metadata["related_concepts"] = data["related_concepts"]
    
    if "links" in data:
        metadata["links"] = data["links"]
    
    # Extract property metadata (non-description fields)
    properties = {}
    
    for section in ["metadata", "spec", "status"]:
        if section not in data:
            continue
        
        section_data = data[section]
        
        # Skip include_properties - those are handled separately
        if "properties" not in section_data:
            continue
        
        for prop in section_data["properties"]:
            prop_name = prop["name"]
            prop_meta = {}
            
            # Extract metadata fields (not descriptions or types)
            if "group" in prop:
                prop_meta["group"] = prop["group"]
            
            if "updatable" in prop:
                prop_meta["updatable"] = prop["updatable"]
            
            if "platforms" in prop:
                prop_meta["platforms"] = prop["platforms"]
            
            if "related_concepts" in prop:
                prop_meta["related_concepts"] = prop["related_concepts"]
            
            if "related_resources" in prop:
                prop_meta["related_resources"] = prop["related_resources"]
            
            if "links" in prop:
                prop_meta["links"] = prop["links"]
            
            if "choices" in prop:
                # Extract choice metadata (name and description, platform notes)
                choices = []
                for choice in prop["choices"]:
                    choice_meta = {"name": choice["name"]}
                    if "description" in choice:
                        choice_meta["description"] = choice["description"]
                    if "platforms" in choice:
                        choice_meta["platforms"] = choice["platforms"]
                    choices.append(choice_meta)
                prop_meta["choices"] = choices
            
            if prop_meta:
                properties[prop_name] = prop_meta
    
    if properties:
        metadata["properties"] = properties
    
    # Write metadata file
    write_yaml_simple(output_path, metadata)
    print(f"Created {output_path}")
    
    return metadata

def main():
    """Extract metadata from all resource YAML files"""
    
    # Check for PyYAML
    try:
        import yaml
        print("PyYAML found - using proper YAML parser")
    except ImportError:
        print("=" * 70)
        print("WARNING: PyYAML not installed!")
        print("Install it with: pip install pyyaml")
        print("=" * 70)
        return 1
    
    config_dir = "config/resources"
    output_dir = "config/resources/metadata"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all YAML files except special ones
    skip_files = ["properties.yaml", "overview.md", "groups.yaml"]
    
    success_count = 0
    error_count = 0
    
    for filename in sorted(os.listdir(config_dir)):
        if not filename.endswith(".yaml"):
            continue
        
        if filename in skip_files:
            continue
        
        input_path = os.path.join(config_dir, filename)
        
        # Skip if it's a directory
        if os.path.isdir(input_path):
            continue
        
        output_path = os.path.join(output_dir, filename)
        
        try:
            result = extract_metadata(input_path, output_path)
            if result:
                success_count += 1
            else:
                error_count += 1
        except Exception as e:
            print(f"ERROR: Failed to process {filename}: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            error_count += 1
    
    print("\n" + "=" * 70)
    print(f"Metadata extraction complete!")
    print(f"Success: {success_count}, Errors: {error_count}")
    print(f"Review files in {output_dir} before proceeding")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Review extracted metadata files")
    print("2. Compare with CRD descriptions")
    print("3. Remove redundant descriptions from metadata")
    print("4. Test generation with: ./plano generate")
    
    return 0 if error_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
