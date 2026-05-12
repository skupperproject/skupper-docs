#!/usr/bin/env python3
"""
Validate resource metadata files against CRDs.

This validates that the extracted metadata is consistent with the CRD definitions.
"""

import os
import sys
import yaml
from pathlib import Path

def load_crd(crd_path):
    """Load and parse a CRD file."""
    with open(crd_path, 'r') as f:
        crd = yaml.safe_load(f)
    
    version = crd['spec']['versions'][0]
    schema = version['schema']['openAPIV3Schema']
    
    result = {
        'kind': crd['spec']['names']['kind'],
        'spec_properties': {},
        'status_properties': {}
    }
    
    # Extract spec properties
    if 'properties' in schema and 'spec' in schema['properties']:
        spec_schema = schema['properties']['spec']
        if 'properties' in spec_schema:
            for prop_name, prop_schema in spec_schema['properties'].items():
                result['spec_properties'][prop_name] = {
                    'type': prop_schema.get('type', 'unknown'),
                    'enum': prop_schema.get('enum', [])
                }
    
    # Extract status properties
    if 'properties' in schema and 'status' in schema['properties']:
        status_schema = schema['properties']['status']
        if 'properties' in status_schema:
            for prop_name, prop_schema in status_schema['properties'].items():
                result['status_properties'][prop_name] = {
                    'type': prop_schema.get('type', 'unknown')
                }
    
    return result

def load_metadata(metadata_path):
    """Load a metadata file."""
    with open(metadata_path, 'r') as f:
        data = yaml.safe_load(f)
    
    result = {
        'name': data.get('name', ''),
        'spec_properties': {},
        'status_properties': {}
    }
    
    # Extract spec properties
    spec_data = data.get('spec', {})
    if 'properties' in spec_data:
        for prop in spec_data['properties']:
            if isinstance(prop, dict) and 'name' in prop:
                prop_name = prop['name']
                result['spec_properties'][prop_name] = {
                    'choices': [c['name'] for c in prop.get('choices', [])]
                }
    
    # Extract status properties
    status_data = data.get('status', {})
    if 'properties' in status_data:
        for prop in status_data['properties']:
            if isinstance(prop, dict) and 'name' in prop:
                prop_name = prop['name']
                result['status_properties'][prop_name] = {}
    
    return result

def camel_to_snake(name):
    """Convert CamelCase to snake_case."""
    import re
    # Insert underscore before uppercase letters (except at start)
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    # Insert underscore before uppercase letters preceded by lowercase
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def find_crd_file(crds_dir, resource_name):
    """Find the CRD file for a resource."""
    # Convert CamelCase to snake_case
    # e.g., "AccessGrant" -> "access_grant"
    snake_name = camel_to_snake(resource_name)
    filename = f"skupper_{snake_name}_crd.yaml"
    path = os.path.join(crds_dir, filename)
    
    if os.path.exists(path):
        return path
    
    return None

def compare_metadata(metadata_data, crd_data, resource_name):
    """Compare metadata with CRD data."""
    issues = []
    
    # Compare spec properties
    metadata_spec_props = set(metadata_data['spec_properties'].keys())
    crd_spec_props = set(crd_data['spec_properties'].keys())
    
    # Properties in metadata but not in CRD
    extra_in_metadata = metadata_spec_props - crd_spec_props
    if extra_in_metadata:
        for prop_name in extra_in_metadata:
            issues.append({
                'type': 'extra_property',
                'severity': 'warning',
                'section': 'spec',
                'property': prop_name,
                'message': f"Property '{prop_name}' in metadata but not in CRD"
            })
    
    # Check enum/choices for common properties
    for prop_name in metadata_spec_props & crd_spec_props:
        metadata_prop = metadata_data['spec_properties'][prop_name]
        crd_prop = crd_data['spec_properties'][prop_name]
        
        if crd_prop['enum'] and metadata_prop['choices']:
            crd_values = set(crd_prop['enum'])
            metadata_choices = set(metadata_prop['choices'])
            
            extra_choices = metadata_choices - crd_values
            if extra_choices:
                issues.append({
                    'type': 'enum_mismatch',
                    'severity': 'warning',
                    'section': 'spec',
                    'property': prop_name,
                    'message': f"Property '{prop_name}' has choices not in CRD enum: {extra_choices}"
                })
            
            missing_choices = crd_values - metadata_choices
            if missing_choices:
                issues.append({
                    'type': 'enum_incomplete',
                    'severity': 'info',
                    'section': 'spec',
                    'property': prop_name,
                    'message': f"Property '{prop_name}' CRD enum values not in metadata: {missing_choices}"
                })
    
    # Compare status properties
    metadata_status_props = set(metadata_data['status_properties'].keys())
    crd_status_props = set(crd_data['status_properties'].keys())
    
    extra_in_metadata_status = metadata_status_props - crd_status_props
    if extra_in_metadata_status:
        for prop_name in extra_in_metadata_status:
            issues.append({
                'type': 'extra_property',
                'severity': 'warning',
                'section': 'status',
                'property': prop_name,
                'message': f"Status property '{prop_name}' in metadata but not in CRD"
            })
    
    return issues

def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    crds_dir = repo_root / "crds"
    metadata_dir = repo_root / "config" / "resources" / "metadata"
    
    if not crds_dir.exists():
        print(f"❌ CRDs directory not found: {crds_dir}")
        return 1
    
    if not metadata_dir.exists():
        print(f"❌ Metadata directory not found: {metadata_dir}")
        return 1
    
    print("🔍 Validating resource metadata against CRDs...\n")
    
    # Load all metadata files
    metadata_files = {}
    for yaml_file in os.listdir(metadata_dir):
        if yaml_file.endswith('.yaml'):
            path = os.path.join(metadata_dir, yaml_file)
            try:
                data = load_metadata(path)
                if data['name']:
                    metadata_files[data['name']] = data
            except Exception as e:
                print(f"⚠️  Error loading {yaml_file}: {e}")
    
    print(f"📋 Loaded {len(metadata_files)} metadata files\n")
    
    all_issues = []
    resources_checked = 0
    resources_missing_crd = 0
    
    # Check each metadata file
    for resource_name, metadata_data in sorted(metadata_files.items()):
        # Find corresponding CRD
        crd_path = find_crd_file(crds_dir, resource_name)
        
        if not crd_path:
            print(f"❌ {resource_name}: No CRD file found")
            resources_missing_crd += 1
            continue
        
        # Load CRD
        try:
            crd_data = load_crd(crd_path)
        except Exception as e:
            print(f"❌ {resource_name}: Error loading CRD: {e}")
            continue
        
        resources_checked += 1
        
        # Compare
        issues = compare_metadata(metadata_data, crd_data, resource_name)
        
        if issues:
            all_issues.extend(issues)
            print(f"⚠️  {resource_name}: {len(issues)} issues")
            for issue in issues:
                severity_icon = "⚠️ " if issue['severity'] == 'warning' else "ℹ️ "
                section = f"[{issue.get('section', 'general')}]" if 'section' in issue else ""
                print(f"    {severity_icon}{section} {issue['message']}")
        else:
            print(f"✅ {resource_name}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 Validation Summary")
    print("="*60)
    print(f"Metadata files checked: {resources_checked}")
    print(f"Resources missing CRD: {resources_missing_crd}")
    print(f"Total issues: {len(all_issues)}")
    
    warnings = [i for i in all_issues if i['severity'] == 'warning']
    infos = [i for i in all_issues if i['severity'] == 'info']
    
    print(f"Warnings: {len(warnings)}")
    print(f"Info: {len(infos)}")
    
    if warnings:
        print("\n⚠️  Warnings indicate potential problems")
    if infos:
        print("ℹ️  Info items are for awareness (may be intentional)")
    
    if len(all_issues) == 0 and resources_missing_crd == 0:
        print("\n✅ All validations passed!")
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())

# Made with Bob
