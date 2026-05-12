#!/usr/bin/env python3
"""
Validate CRD definitions against YAML resource configs.

This shows what would change if we switched to CRDs as the source of truth.
"""

import os
import sys
import yaml
from pathlib import Path

def load_crd(crd_path):
    """Load and parse a CRD file."""
    with open(crd_path, 'r') as f:
        crd = yaml.safe_load(f)
    
    # Extract the schema
    version = crd['spec']['versions'][0]
    schema = version['schema']['openAPIV3Schema']
    
    result = {
        'kind': crd['spec']['names']['kind'],
        'description': schema.get('description', ''),
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
                    'description': prop_schema.get('description', ''),
                    'enum': prop_schema.get('enum', [])
                }
    
    # Extract status properties
    if 'properties' in schema and 'status' in schema['properties']:
        status_schema = schema['properties']['status']
        if 'properties' in status_schema:
            for prop_name, prop_schema in status_schema['properties'].items():
                result['status_properties'][prop_name] = {
                    'type': prop_schema.get('type', 'unknown'),
                    'description': prop_schema.get('description', '')
                }
    
    return result

def load_yaml_resource(yaml_path):
    """Load a YAML resource config."""
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    result = {
        'name': data.get('name', ''),
        'description': data.get('description', ''),
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
                    'description': prop.get('description', ''),
                    'choices': prop.get('choices', []),
                    'default': prop.get('default'),
                    'type': prop.get('type')
                }
    
    # Extract status properties
    status_data = data.get('status', {})
    if 'properties' in status_data:
        for prop in status_data['properties']:
            if isinstance(prop, dict) and 'name' in prop:
                prop_name = prop['name']
                result['status_properties'][prop_name] = {
                    'description': prop.get('description', '')
                }
    
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
    # Convert resource name to CRD filename
    # e.g., "Site" -> "skupper_site_crd.yaml"
    # e.g., "AccessGrant" -> "skupper_access_grant_crd.yaml"
    snake_name = camel_to_snake(resource_name)
    filename = f"skupper_{snake_name}_crd.yaml"
    path = os.path.join(crds_dir, filename)
    
    if os.path.exists(path):
        return path
    
    return None

def compare_descriptions(yaml_desc, crd_desc):
    """Compare descriptions (normalize whitespace)."""
    yaml_normalized = ' '.join(yaml_desc.split())
    crd_normalized = ' '.join(crd_desc.split())
    
    # Check if YAML description is a subset or similar
    if yaml_normalized.lower() in crd_normalized.lower():
        return True
    if crd_normalized.lower() in yaml_normalized.lower():
        return True
    
    # Check for significant differences
    yaml_words = set(yaml_normalized.lower().split())
    crd_words = set(crd_normalized.lower().split())
    
    common = yaml_words & crd_words
    if len(common) / max(len(yaml_words), len(crd_words)) > 0.7:
        return True
    
    return False

def compare_resource(yaml_data, crd_data, resource_name):
    """Compare YAML config with CRD data."""
    issues = []
    
    # Compare descriptions
    if yaml_data['description'] and crd_data['description']:
        if not compare_descriptions(yaml_data['description'], crd_data['description']):
            issues.append({
                'type': 'description_diff',
                'severity': 'info',
                'message': 'Description differs significantly from CRD'
            })
    
    # Compare spec properties
    yaml_spec_props = set(yaml_data['spec_properties'].keys())
    crd_spec_props = set(crd_data['spec_properties'].keys())
    
    # Properties in YAML but not in CRD
    extra_in_yaml = yaml_spec_props - crd_spec_props
    if extra_in_yaml:
        for prop_name in extra_in_yaml:
            issues.append({
                'type': 'extra_property',
                'severity': 'warning',
                'section': 'spec',
                'property': prop_name,
                'message': f"Property '{prop_name}' in YAML but not in CRD"
            })
    
    # Properties in CRD but not in YAML
    missing_in_yaml = crd_spec_props - yaml_spec_props
    if missing_in_yaml:
        for prop_name in missing_in_yaml:
            issues.append({
                'type': 'missing_property',
                'severity': 'info',
                'section': 'spec',
                'property': prop_name,
                'message': f"Property '{prop_name}' in CRD but not documented in YAML"
            })
    
    # Compare property details for common properties
    for prop_name in yaml_spec_props & crd_spec_props:
        yaml_prop = yaml_data['spec_properties'][prop_name]
        crd_prop = crd_data['spec_properties'][prop_name]
        
        # Check enum/choices
        if crd_prop['enum']:
            crd_values = set(crd_prop['enum'])
            yaml_choices = set(c['name'] for c in yaml_prop.get('choices', []))
            
            extra_choices = yaml_choices - crd_values
            if extra_choices:
                issues.append({
                    'type': 'enum_mismatch',
                    'severity': 'warning',
                    'section': 'spec',
                    'property': prop_name,
                    'message': f"Property '{prop_name}' has choices not in CRD enum: {extra_choices}"
                })
            
            missing_choices = crd_values - yaml_choices
            if missing_choices:
                issues.append({
                    'type': 'enum_incomplete',
                    'severity': 'info',
                    'section': 'spec',
                    'property': prop_name,
                    'message': f"Property '{prop_name}' CRD enum values not documented: {missing_choices}"
                })
        
        # Check type if specified in YAML
        if yaml_prop.get('type') and crd_prop['type']:
            yaml_type = yaml_prop['type'].lower()
            crd_type = crd_prop['type'].lower()
            
            # Map common type variations
            type_map = {
                'bool': 'boolean',
                'int': 'integer',
                'str': 'string'
            }
            yaml_type = type_map.get(yaml_type, yaml_type)
            
            if yaml_type != crd_type:
                issues.append({
                    'type': 'type_mismatch',
                    'severity': 'warning',
                    'section': 'spec',
                    'property': prop_name,
                    'message': f"Property '{prop_name}' type mismatch: YAML={yaml_type}, CRD={crd_type}"
                })
    
    # Compare status properties
    yaml_status_props = set(yaml_data['status_properties'].keys())
    crd_status_props = set(crd_data['status_properties'].keys())
    
    extra_in_yaml_status = yaml_status_props - crd_status_props
    if extra_in_yaml_status:
        for prop_name in extra_in_yaml_status:
            issues.append({
                'type': 'extra_property',
                'severity': 'warning',
                'section': 'status',
                'property': prop_name,
                'message': f"Status property '{prop_name}' in YAML but not in CRD"
            })
    
    missing_in_yaml_status = crd_status_props - yaml_status_props
    if missing_in_yaml_status:
        for prop_name in missing_in_yaml_status:
            issues.append({
                'type': 'missing_property',
                'severity': 'info',
                'section': 'status',
                'property': prop_name,
                'message': f"Status property '{prop_name}' in CRD but not documented in YAML"
            })
    
    return issues

def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    crds_dir = repo_root / "crds"
    config_dir = repo_root / "config" / "resources"
    
    if not crds_dir.exists():
        print(f"❌ CRDs directory not found: {crds_dir}")
        return 1
    
    if not config_dir.exists():
        print(f"❌ Config directory not found: {config_dir}")
        return 1
    
    print("🔍 Validating YAML resource configs against CRDs...\n")
    
    # Load all YAML resources
    yaml_resources = {}
    for yaml_file in os.listdir(config_dir):
        if yaml_file.endswith('.yaml') and yaml_file not in ['properties.yaml', 'groups.yaml', 'overview.md']:
            path = os.path.join(config_dir, yaml_file)
            try:
                data = load_yaml_resource(path)
                if data['name']:
                    yaml_resources[data['name']] = data
            except Exception as e:
                print(f"⚠️  Error loading {yaml_file}: {e}")
    
    print(f"📋 Loaded {len(yaml_resources)} YAML resource configs\n")
    
    all_issues = []
    resources_checked = 0
    resources_missing_crd = 0
    
    # Check each YAML resource
    for resource_name, yaml_data in sorted(yaml_resources.items()):
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
        issues = compare_resource(yaml_data, crd_data, resource_name)
        
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
    print(f"Resources checked: {resources_checked}")
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
