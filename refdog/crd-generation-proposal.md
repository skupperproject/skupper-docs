# Proposal: Generate Documentation Directly from CRDs

## Executive Summary

**Recommendation**: Yes, it's feasible and beneficial to generate documentation directly from CRDs instead of maintaining separate YAML configuration files.

**Benefits**:
- Single source of truth (CRDs)
- No manual sync required
- Descriptions stay current with API changes
- Reduced maintenance burden
- Automatic consistency

**Trade-offs**:
- Less control over documentation formatting
- Need to enhance CRD descriptions for documentation quality
- Examples must be stored separately or embedded in CRDs

## Current Architecture

### What We Have Now

```
config/resources/*.yaml  (Human-maintained)
    ↓
python/resources.py (Generation)
    ↓
input/resources/*.md (Generated docs)
```

**YAML configs contain**:
- Resource descriptions
- Property descriptions
- Examples
- Grouping (frequently-used, advanced)
- Cross-references (related_resources, related_concepts, links)
- Default values
- Updatable flags
- Platform-specific notes

**CRDs contain**:
- OpenAPI schema
- Property types
- Descriptions (NOW AVAILABLE!)
- Required fields
- Validation rules
- Default values (in some cases)

## Proposed Architecture

### Option 1: Pure CRD Generation (Recommended)

```
crds/*.yaml (Single source of truth)
    ↓
python/resources.py (Enhanced generation)
    ↓
input/resources/*.md (Generated docs)
```

**What needs to be added to CRDs**:
- Examples (as annotations or separate files)
- Documentation metadata (grouping, cross-references)
- Enhanced descriptions where needed

### Option 2: Hybrid Approach

```
crds/*.yaml (Technical definitions + descriptions)
    +
config/resources/metadata.yaml (Documentation metadata only)
    ↓
python/resources.py (Enhanced generation)
    ↓
input/resources/*.md (Generated docs)
```

**Metadata file would contain**:
- Examples
- Cross-references (related_resources, related_concepts)
- External links
- Property grouping (frequently-used, advanced)
- Overview text

## What CRDs Already Provide

### ✅ Available in CRDs

1. **Resource-level descriptions**: 
   ```yaml
   openAPIV3Schema:
     description: |-
       A site is a place on the network where application workloads are
       running. Sites are joined by links.
   ```

2. **Property descriptions**:
   ```yaml
   linkAccess:
     description: |-
       Configure external access for links from remote sites...
   ```

3. **Property types**: `string`, `boolean`, `integer`, `object`, `array`

4. **Property formats**: `duration`, `date-time`

5. **Required fields**: 
   ```yaml
   required:
   - routingKey
   - port
   ```

6. **Validation constraints**: `enum`, `pattern`, `minimum`, `maximum`

7. **Default values** (in some properties)

8. **Nested object structures**

### ❌ Missing from CRDs (Need to Add)

1. **Examples**: No standard place for usage examples
2. **Property grouping**: No "frequently-used" vs "advanced" distinction
3. **Cross-references**: No links to related resources/concepts
4. **External links**: No references to external documentation
5. **Updatable flags**: No indication if property can be changed after creation
6. **Platform-specific notes**: No Kubernetes vs Docker/Podman distinctions
7. **Choice descriptions**: Enum values lack detailed descriptions

## Implementation Approaches

### Approach A: Use CRD Annotations (Kubernetes-Native)

Add documentation metadata as annotations:

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: sites.skupper.io
  annotations:
    skupper.io/examples: |
      - description: A minimal site
        yaml: |
          apiVersion: skupper.io/v2alpha1
          kind: Site
          ...
    skupper.io/related-resources: "link,listener,connector"
    skupper.io/related-concepts: "network,platform"
spec:
  versions:
    - name: v2alpha1
      schema:
        openAPIV3Schema:
          properties:
            spec:
              properties:
                linkAccess:
                  description: ...
                  x-skupper-group: frequently-used
                  x-skupper-updatable: true
                  x-skupper-related-concepts: "link"
```

**Pros**:
- Keeps everything in CRD files
- Uses Kubernetes extension mechanism (`x-` prefix)
- Single source of truth

**Cons**:
- CRD files become larger
- Non-standard use of annotations
- Harder to edit/maintain

### Approach B: Separate Metadata Files (Recommended)

Keep CRDs clean, add minimal metadata files:

```yaml
# config/resources/metadata/site.yaml
name: Site
examples:
  - description: A minimal site
    yaml: |
      apiVersion: skupper.io/v2alpha1
      kind: Site
      ...

related_resources: [link, listener, connector]
related_concepts: [network, platform]
links: [skupper/site-configuration]

properties:
  linkAccess:
    group: frequently-used
    updatable: true
    related_concepts: [link]
    links: [skupper/site-linking]
  
  ha:
    updatable: true
    platforms: [Kubernetes]
    links: [skupper/high-availability]
```

**Pros**:
- CRDs stay clean and standard
- Easy to edit metadata
- Clear separation of concerns
- Smaller files

**Cons**:
- Two files to maintain (but much simpler than current YAML)
- Need to merge data during generation

### Approach C: Examples in Separate Directory

```
crds/
  skupper_site_crd.yaml
  skupper_connector_crd.yaml
  ...

config/resources/
  examples/
    site.yaml          # Just examples
    connector.yaml
  metadata/
    site.yaml          # Just metadata (grouping, links)
    connector.yaml
```

**Pros**:
- Very clean separation
- Examples easy to test
- Metadata minimal

**Cons**:
- Three places to look (CRD, examples, metadata)

## Recommended Implementation Plan

### Phase 1: Enhance CRD Descriptions (If Needed)

1. Review all CRD descriptions for completeness
2. Add missing descriptions
3. Ensure descriptions are documentation-quality
4. Add choice descriptions for enum values

### Phase 2: Create Minimal Metadata Files

1. Create `config/resources/metadata/` directory
2. For each resource, create a metadata file with:
   - Examples
   - Cross-references (related_resources, related_concepts)
   - External links
   - Property grouping (frequently-used, advanced)
   - Updatable flags
   - Platform-specific notes

Example structure:
```yaml
# config/resources/metadata/site.yaml
examples:
  - description: A minimal site
    yaml: |
      apiVersion: skupper.io/v2alpha1
      kind: Site
      metadata:
        name: east
        namespace: hello-world-east

related_resources: [link]
related_concepts: [network, platform]
links: [skupper/site-configuration]

properties:
  linkAccess:
    group: frequently-used
    updatable: true
    related_concepts: [link]
  ha:
    updatable: true
  defaultIssuer:
    group: advanced
    updatable: true
  edge:
    group: advanced
  serviceAccount:
    group: advanced
  settings:
    group: advanced
```

### Phase 3: Modify Generation Code

Update `python/resources.py` to:

1. **Load CRDs** (already done)
2. **Load metadata files** (new)
3. **Merge data**:
   - Use CRD for: descriptions, types, required fields, validation
   - Use metadata for: examples, grouping, cross-references, links
4. **Generate markdown** (similar to current process)

Key changes needed:

```python
class ResourceModel(Model):
    def __init__(self):
        super().__init__(Resource, "config/resources/metadata")  # Changed path
        
        # Load CRDs (already exists)
        self.crds_by_name = dict()
        for crd_file in list_dir("crds"):
            # ... existing code ...
        
        # Load metadata files (new)
        self.metadata_by_name = dict()
        for metadata_file in list_dir("config/resources/metadata"):
            data = read_yaml(join("config/resources/metadata", metadata_file))
            self.metadata_by_name[data["name"]] = data

class Resource(ModelObject):
    def __init__(self, model, crd_data, metadata_data):
        # Merge CRD schema with metadata
        self.name = crd_data["spec"]["names"]["kind"]
        self.description = crd_data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["description"]
        self.examples = metadata_data.get("examples", [])
        self.related_resources = metadata_data.get("related_resources", [])
        # ... etc
        
        # Extract properties from CRD schema
        schema = crd_data["spec"]["versions"][0]["schema"]["openAPIV3Schema"]
        for prop_name, prop_schema in schema["properties"]["spec"]["properties"].items():
            prop_metadata = metadata_data.get("properties", {}).get(prop_name, {})
            prop = Property(
                name=prop_name,
                type=prop_schema.get("type"),
                description=prop_schema.get("description"),
                group=prop_metadata.get("group"),
                updatable=prop_metadata.get("updatable"),
                # ... merge CRD and metadata
            )
            self.spec_properties.append(prop)
```

### Phase 4: Migration

1. **Create metadata files** from existing YAML configs (extract non-CRD data)
2. **Test generation** with new code
3. **Compare output** with current generated docs
4. **Iterate** until output matches or improves
5. **Remove old YAML configs** once satisfied

### Phase 5: Update Workflow

1. Update `./plano update_crds` to also validate metadata files
2. Update documentation (resources.md)
3. Update contributor guidelines

## Migration Script

Create a script to extract metadata from current YAML configs:

```python
# scripts/extract_metadata.py
import yaml

def extract_metadata(yaml_config_path):
    """Extract non-CRD data from existing YAML config"""
    with open(yaml_config_path) as f:
        data = yaml.safe_load(f)
    
    metadata = {
        "examples": data.get("examples", []),
        "related_resources": data.get("related_resources", []),
        "related_concepts": data.get("related_concepts", []),
        "links": data.get("links", []),
        "properties": {}
    }
    
    # Extract property metadata
    for section in ["spec", "status"]:
        if section in data:
            for prop in data[section].get("properties", []):
                prop_meta = {}
                if "group" in prop:
                    prop_meta["group"] = prop["group"]
                if "updatable" in prop:
                    prop_meta["updatable"] = prop["updatable"]
                if "related_concepts" in prop:
                    prop_meta["related_concepts"] = prop["related_concepts"]
                if "related_resources" in prop:
                    prop_meta["related_resources"] = prop["related_resources"]
                if "links" in prop:
                    prop_meta["links"] = prop["links"]
                if "platforms" in prop:
                    prop_meta["platforms"] = prop["platforms"]
                
                if prop_meta:
                    metadata["properties"][prop["name"]] = prop_meta
    
    return metadata
```

## Benefits of This Approach

1. **Single Source of Truth**: CRDs are authoritative for schema and descriptions
2. **Reduced Duplication**: No need to maintain descriptions in two places
3. **Automatic Sync**: Descriptions update automatically when CRDs update
4. **Simpler Maintenance**: Metadata files are much smaller than current YAML configs
5. **Better Consistency**: Schema and docs always match
6. **Easier Updates**: Update CRD descriptions in Skupper repo, they flow through automatically

## Risks and Mitigations

### Risk 1: CRD Descriptions Not Documentation-Quality

**Mitigation**: 
- Review and enhance CRD descriptions before migration
- Establish guidelines for CRD description quality
- Can still override in metadata if needed

### Risk 2: Loss of Documentation Control

**Mitigation**:
- Metadata files provide override capability
- Can add supplementary text in metadata
- Examples remain fully controllable

### Risk 3: Breaking Existing Workflow

**Mitigation**:
- Phased migration approach
- Keep old system working during transition
- Extensive testing before cutover

## Estimated Effort

- **Phase 1** (Enhance CRDs): 2-4 hours (review and update descriptions)
- **Phase 2** (Create metadata files): 4-6 hours (extract from existing YAML)
- **Phase 3** (Modify generation code): 8-12 hours (rewrite resource loading/merging)
- **Phase 4** (Migration/testing): 4-6 hours (validate output, fix issues)
- **Phase 5** (Documentation): 2-3 hours (update resources.md)

**Total**: 20-31 hours

## Recommendation

**Proceed with Approach B (Separate Metadata Files)**:

1. ✅ Keeps CRDs clean and standard
2. ✅ Minimal metadata files (much simpler than current YAML)
3. ✅ Clear separation: CRDs = schema/descriptions, Metadata = doc structure
4. ✅ Easy to maintain and understand
5. ✅ Preserves flexibility for documentation needs

**Next Steps**:
1. Review CRD descriptions for quality
2. Create migration script to extract metadata
3. Implement enhanced generation code
4. Test with one resource (e.g., Site)
5. Migrate remaining resources
6. Update documentation

This approach gives you the best of both worlds: authoritative descriptions from CRDs with minimal metadata for documentation structure.