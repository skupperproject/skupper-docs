#!/usr/bin/env python3
"""
Extract metadata from existing YAML config files to create minimal metadata files.
"""

import os
import sys

# Add python directory to path to import plano
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python"))
from plano import read_yaml, emit_yaml

def extract_metadata(yaml_config_path, output_path):
    """Extract non-CRD data from existing YAML config"""
    print(f"Extracting metadata from {yaml_config_path}")
    
    data = read_yaml(yaml_config_path)
    
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
    emit_yaml(output_path, metadata)
    
    print(f"Created {output_path}")
    
    return metadata

def main():
    """Extract metadata from all resource YAML files"""
    config_dir = "config/resources"
    output_dir = "config/resources/metadata"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all YAML files except special ones
    skip_files = ["properties.yaml", "overview.md"]
    
    for filename in os.listdir(config_dir):
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
            extract_metadata(input_path, output_path)
        except Exception as e:
            print(f"ERROR: Failed to process {filename}: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
    
    print("\nMetadata extraction complete!")
    print(f"Review files in {output_dir} before proceeding")
    print("\nNext steps:")
    print("1. Review extracted metadata files")
    print("2. Compare with CRD descriptions")
    print("3. Remove redundant descriptions from metadata")
    print("4. Test generation with: ./plano generate")

if __name__ == "__main__":
    main()

# Made with Bob
