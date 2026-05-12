# Custom Resource (CR) Management Processes

This document describes all processes relating to Custom Resources (CRs) and resources in the Refdog documentation system.

## Overview

The Refdog system maintains documentation for Skupper Custom Resources through a dual-source approach:

1. **YAML Configuration Files** (`config/resources/*.yaml`) - Human-maintained source of truth for documentation
2. **CRD Files** (`crds/*.yaml`) - Technical definitions from the Skupper repository
3. **Generated Markdown** (`input/resources/*.md`) - Auto-generated documentation from YAML configs

## Architecture

### Source Files

#### 1. YAML Configuration Files (`config/resources/`)

These are the primary source for resource documentation:

- **Location**: `config/resources/`
- **Format**: YAML files, one per resource type
- **Purpose**: Define human-readable documentation, examples, property descriptions
- **Examples**:
  - `site.yaml` - Site resource documentation
  - `connector.yaml` - Connector resource documentation
  - `listener.yaml` - Listener resource documentation
  - `link.yaml` - Link resource documentation
  - `access-grant.yaml` - AccessGrant resource documentation
  - `access-token.yaml` - AccessToken resource documentation
  - `router-access.yaml` - RouterAccess resource documentation
  - `attached-connector.yaml` - AttachedConnector resource documentation
  - `attached-connector-binding.yaml` - AttachedConnectorBinding resource documentation

#### 2. Shared Properties (`config/resources/properties.yaml`)

Common property definitions shared across multiple resources:

- **Location**: `config/resources/properties.yaml`
- **Purpose**: Define reusable property documentation (e.g., `metadata/name`, `status/status`, `settings`)
- **Usage**: Referenced by individual resource YAML files using `include_properties`

#### 3. Overview Documentation (`config/resources/overview.md`)

- **Location**: `config/resources/overview.md`
- **Purpose**: Provides general information about Skupper resources, controller behavior, and operations
- **Integration**: Appended to the generated resource index page

#### 4. CRD Files (`crds/`)

Technical Kubernetes Custom Resource Definitions:

- **Location**: `crds/`
- **Source**: Skupper repository (`skupperproject/skupper`)
- **Format**: Kubernetes CRD YAML files
- **Purpose**: Define the actual API schema, validation rules, and OpenAPI specifications
- **Examples**:
  - `skupper_site_crd.yaml`
  - `skupper_connector_crd.yaml`
  - `skupper_listener_crd.yaml`
  - `skupper_link_crd.yaml`
  - etc.

### Generated Files

#### Generated Markdown (`input/resources/`)

- **Location**: `input/resources/`
- **Generated From**: YAML configuration files
- **Generator**: `python/resources.py`
- **Output**: Markdown files with structured property documentation
- **Examples**:
  - `site.md`
  - `connector.md`
  - `listener.md`
  - etc.

## YAML Configuration Structure

Each resource YAML file follows this structure:

```yaml
name: ResourceName                    # Display name
related_resources: [other-resource]   # Links to related resources
links: [external/link/reference]      # External documentation links
description: |                        # Resource description
  Multi-line description text

examples:                             # Usage examples
  - description: Example description
    yaml: |
      apiVersion: skupper.io/v2alpha1
      kind: ResourceName
      # ... example YAML

metadata:                             # Metadata properties section
  include_properties: [metadata/*]    # Include common properties
  properties:                         # Resource-specific properties
    - name: propertyName
      # ... property definition

spec:                                 # Spec properties section
  include_properties: [settings]      # Include common properties
  properties:
    - name: propertyName
      group: frequently-used          # Property grouping
      default: defaultValue           # Default value
      updatable: true                 # Can be updated after creation
      type: string                    # Data type
      platforms: [Kubernetes]         # Platform availability
      related_concepts: [concept]     # Related concept links
      links: [external/link]          # External links
      description: |
        Property description
      choices:                        # For enum properties
        - name: choiceName
          description: Choice description

status:                               # Status properties section
  include_properties: [status/*]      # Include common properties
  properties:
    - name: propertyName
      group: advanced                 # Property grouping
      description: |
        Property description
```

### Property Groups

Properties can be organized into groups that affect their display:

- **`required`**: Required properties (shown first, expanded)
- **`frequently-used`**: Commonly used properties (shown expanded)
- **`None`** (default): Standard properties (shown expanded)
- **`advanced`**: Advanced properties (shown collapsed by default)

### Property Attributes

- `name`: Property name (required)
- `type`: Data type (string, boolean, integer, object, array)
- `format`: Type format (e.g., date-time)
- `group`: Display grouping (required, frequently-used, advanced)
- `default`: Default value
- `updatable`: Whether the property can be updated after creation
- `required`: Whether the property is required
- `platforms`: Platform availability (Kubernetes, Docker, Podman, Linux)
- `hidden`: Hide from documentation
- `description`: Human-readable description
- `choices`: For enum types, list of valid values
- `related_concepts`: Links to related concept pages
- `related_resources`: Links to related resource pages
- `links`: External documentation links
- `notes`: Internal notes (not displayed)

## Processes

### 1. Updating CRDs from Skupper Repository

**Command**: `./plano update_crds`

**Purpose**: Fetch the latest CRD definitions from the Skupper repository

**Process**:
1. Downloads the Skupper v2 branch as a tarball from GitHub
2. Extracts the archive to a temporary directory
3. Copies CRD files from `api/types/crds` to the local `crds/` directory
4. Overwrites existing CRD files

**Source**: `.plano.py` lines 30-48

**When to Use**:
- After Skupper repository updates that modify CRD schemas
- When adding support for new resource types
- When CRD validation rules change

**URL**: `https://github.com/skupperproject/skupper/archive/refs/heads/main.tar.gz`

### 2. Generating Documentation from YAML

**Command**: `./plano generate`

**Purpose**: Generate markdown documentation from YAML configuration files

**Process**:
1. Loads all resource YAML files from `config/resources/`
2. Loads shared properties from `config/resources/properties.yaml`
3. Loads CRD files from `crds/` for validation
4. For each resource:
   - Merges resource-specific and shared property definitions
   - Generates structured markdown with property tables
   - Includes examples, descriptions, and metadata
   - Creates cross-references to related resources and concepts
5. Generates resource index page (`input/resources/index.md`)
6. Validates that YAML configs match CRD schemas

**Source**: `python/resources.py`, `python/generate.py`

**Output Files**:
- `input/resources/index.md` - Resource index page
- `input/resources/<resource-name>.md` - Individual resource pages

**When to Use**:
- After modifying any YAML configuration file
- After updating resource descriptions or examples
- After adding new properties or resources
- Before committing documentation changes

### 3. Validation and Consistency Checking

**Automatic**: Runs as part of `./plano generate`

**Purpose**: Ensure YAML configurations match CRD schemas

**Checks Performed**:
1. **Missing Resources**: Warns if a CRD exists without corresponding YAML config
2. **Extra Resources**: Warns if a YAML config exists without corresponding CRD
3. **Missing Properties**: Warns if CRD defines properties not documented in YAML
4. **Extra Properties**: Warns if YAML documents properties not in CRD

**Source**: `python/resources.py` lines 177-206 (`ResourceModel.check()`)

**Output**: Warning messages for any inconsistencies

**Important Notes**:
- The validation only checks for property **existence**, not description content
- CRDs now include descriptions in their OpenAPI schema, but these are **not automatically synced** to YAML configs
- You must manually keep descriptions in sync between CRDs and YAML configs

### 4. Syncing CRD Descriptions to YAML Configs

**When CRDs Include Descriptions**: The Skupper CRDs now include description fields in their OpenAPI schemas. These descriptions should be kept in sync with the YAML configuration files.

**Manual Sync Process**:

1. **After updating CRDs** (`./plano update_crds`), review the CRD files for new or changed descriptions:
   ```bash
   # Check for descriptions in a specific CRD
   grep -A 3 "description:" crds/skupper_site_crd.yaml
   ```

2. **Compare CRD descriptions with YAML configs**:
   - CRD descriptions are in: `crds/<resource>_crd.yaml` under `spec.versions[0].schema.openAPIV3Schema.properties`
   - YAML descriptions are in: `config/resources/<resource>.yaml` under property definitions

3. **Update YAML configs** to match CRD descriptions:
   - Edit `config/resources/<resource>.yaml`
   - Update the `description` field for each property
   - Maintain consistency in formatting and terminology

4. **Regenerate documentation**:
   ```bash
   ./plano generate
   ```

5. **Review changes**:
   - Check generated markdown files in `input/resources/`
   - Verify descriptions are accurate and complete

**Example Comparison**:

CRD description (in `crds/skupper_site_crd.yaml`):
```yaml
linkAccess:
  description: |-
    Configure external access for links from remote sites. When
    set, implies a RouterAccess resource with accessType set
    according to the linkAccess value.
```

YAML config (in `config/resources/site.yaml`):
```yaml
- name: linkAccess
  description: |
    Configure external access for links from remote sites.
    
    Sites and links are the basis for creating application
    networks...
```

**Best Practices for Sync**:
- Keep descriptions concise but complete
- Use the CRD description as the authoritative source
- Add additional context in YAML if needed for documentation
- Mark advanced properties with "Advanced." prefix in descriptions
- Include default values in descriptions when relevant

### 5. Adding a New Resource

**Steps**:

1. **Update CRDs** (if new resource in Skupper):
   ```bash
   ./plano update_crds
   ```

2. **Create YAML Configuration**:
   - Create `config/resources/<resource-name>.yaml`
   - Define resource metadata, description, and examples
   - Document all spec and status properties
   - Reference shared properties where applicable
   - Add related resources and concepts

3. **Generate Documentation**:
   ```bash
   ./plano generate
   ```

4. **Review Output**:
   - Check `input/resources/<resource-name>.md`
   - Verify property documentation is complete
   - Check for validation warnings

5. **Test**:
   ```bash
   ./plano test
   ```

### 6. Updating an Existing Resource

**Steps**:

1. **Update CRDs** (if Skupper schema changed):
   ```bash
   ./plano update_crds
   ```

2. **Modify YAML Configuration**:
   - Edit `config/resources/<resource-name>.yaml`
   - Update descriptions, examples, or property definitions
   - Add/remove properties as needed

3. **Regenerate Documentation**:
   ```bash
   ./plano generate
   ```

4. **Review Changes**:
   - Check generated markdown for correctness
   - Address any validation warnings

5. **Test**:
   ```bash
   ./plano test
   ```

### 7. Updating Shared Properties

**Steps**:

1. **Edit Shared Properties**:
   - Modify `config/resources/properties.yaml`
   - Update property definitions used across multiple resources

2. **Regenerate All Documentation**:
   ```bash
   ./plano generate
   ```
   - All resources using the shared property will be updated

3. **Review Impact**:
   - Check multiple resource pages to verify changes
   - Ensure consistency across all affected resources

### 8. Full Documentation Build and Test

**Command**: `./plano test`

**Process**:
1. Generates documentation from YAML configs
2. Renders HTML from markdown
3. Checks all internal and external links

**When to Use**:
- Before committing changes
- To verify complete documentation integrity
- After major updates

## File Relationships

```
config/resources/
├── properties.yaml          → Shared property definitions
├── overview.md             → General resource documentation
├── site.yaml              ┐
├── connector.yaml         │
├── listener.yaml          ├→ Generate → input/resources/*.md
├── link.yaml              │
└── ...                    ┘

crds/
├── skupper_site_crd.yaml      ┐
├── skupper_connector_crd.yaml ├→ Validation reference
└── ...                        ┘

python/
├── resources.py           → Generation logic
├── generate.py           → Main generation script
└── common.py            → Shared utilities
```

## Code Components

### Python Modules

#### `python/resources.py`

**Key Classes**:
- `ResourceModel`: Manages all resources, loads YAML and CRD files, performs validation
- `Resource`: Represents a single resource with properties
- `Property`: Represents a resource property with metadata

**Key Functions**:
- `generate(model)`: Main generation function, creates index and individual resource pages
- `generate_resource(resource)`: Generates markdown for a single resource
- `generate_property(prop, append)`: Generates markdown for a property

#### `python/generate.py`

**Functions**:
- `generate_objects()`: Orchestrates generation of concepts, resources, and commands
- `generate_index()`: Creates main index page

#### `python/common.py`

**Utilities**:
- `generate_object_metadata(obj)`: Creates frontmatter metadata for pages
- `make_fragment_id(name)`: Generates HTML anchor IDs
- YAML reading/writing functions
- Link management

### Plano Commands

Defined in `.plano.py`:

- `generate`: Generate documentation from YAML configs
- `update_crds`: Update CRD files from Skupper repository
- `test`: Full build and validation
- `render`: Render HTML from markdown
- `check_links`: Validate all links

## Best Practices

### Documentation Maintenance

1. **Keep YAML and CRDs in Sync**:
   - Run `./plano update_crds` regularly
   - Address validation warnings promptly
   - Document all CRD properties in YAML

2. **Use Shared Properties**:
   - Define common properties once in `properties.yaml`
   - Reference them using `include_properties`
   - Maintain consistency across resources

3. **Provide Complete Examples**:
   - Include minimal and advanced examples
   - Show real-world usage patterns
   - Document all common configurations

4. **Group Properties Appropriately**:
   - Mark required properties explicitly
   - Use `frequently-used` for common properties
   - Mark advanced properties to reduce clutter

5. **Cross-Reference Related Content**:
   - Link to related resources
   - Reference relevant concepts
   - Include external documentation links

### Workflow

1. **Before Making Changes**:
   - Update CRDs if Skupper changed
   - Review current documentation
   - Check for related resources

2. **While Making Changes**:
   - Edit YAML configuration files
   - Keep descriptions clear and concise
   - Add examples for new features

3. **After Making Changes**:
   - Run `./plano generate`
   - Review generated markdown
   - Address validation warnings
   - Run `./plano test`
   - Commit both YAML and generated files

## Troubleshooting

### Common Issues

**Validation Warnings**:
- **"Property X is missing"**: Add property to YAML config
- **"Property X is extra"**: Remove from YAML or update CRD
- **"Resource X is missing"**: Create YAML config file
- **"Resource X is extra"**: Remove YAML or add to CRDs

**Generation Errors**:
- Check YAML syntax
- Verify property references exist
- Ensure required fields are present

**Link Errors**:
- Verify link references in `config/links.yaml`
- Check related resource/concept names
- Ensure referenced files exist

## Future Enhancements

Potential improvements to the CR management process:

1. **Automated CRD Sync**: Trigger CRD updates on Skupper releases
2. **Automated Description Sync**: Extract descriptions from CRDs and update YAML configs automatically
3. **Description Diff Tool**: Compare CRD descriptions with YAML descriptions and report differences
4. **Schema Validation**: Validate YAML configs against JSON schema
5. **Diff Reporting**: Show what changed between CRD versions
6. **Property Coverage**: Report on documentation completeness
7. **Example Validation**: Validate example YAML against CRD schemas
8. **Automated Testing**: Test examples against live Skupper installations

## References

- **Skupper Repository**: https://github.com/skupperproject/skupper
- **CRD Source**: `skupperproject/skupper/api/types/crds`
- **Kubernetes CRDs**: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
- **OpenAPI Schema**: https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#validation