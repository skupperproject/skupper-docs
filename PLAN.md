# Integration Plan: Refdog Reference Documentation → Skupper Website

**Goal**: Integrate automatically-generated Skupper reference documentation (commands and resources) into the main Skupper documentation website.

**Current State**: 
- Refdog generates reference docs in `docs-vale/refdog/input/`
- Website uses MkDocs at `website-mkdocs/`
- No integration exists yet

---

## Executive Summary

### Recommended Approach: **Option 2 - MkDocs Integration via Symlinks + Post-Processing**

**Why**:
- ✅ Simple and maintainable
- ✅ Single source of truth (refdog)
- ✅ Works with MkDocs build process
- ✅ No duplication or sync issues
- ✅ Can integrate incrementally
- ✅ Refdog remains independent (can still publish standalone site)

**MkDocs Compatibility**:
- ✅ Fixed with `fix-refdog-for-mkdocs.sh` script
- Removes `{{site.prefix}}` Transom syntax incompatible with MkDocs macros plugin
- Run after `./plano generate` to make output MkDocs-compatible

**Effort**: 2-3 hours (+ 10 minutes for compatibility script)

**Timeline**:
- Phase 1: Commands integration (1 hour) - Production ready now
- Phase 2: Resources integration (1 hour) - After CRD implementation
- Phase 3: Polish and navigation (1 hour)

---

## Current Architecture

### Refdog (docs-vale/refdog/)

```
refdog/
├── cli-doc/              # Source: CLI help from Skupper
├── crds/                 # Source: CRDs from Skupper API
├── config/               # Configuration for generation
├── python/               # Generation code
├── input/                # Generated markdown ✅ THIS IS WHAT WE NEED
│   ├── commands/         # 43 command reference pages
│   │   ├── index.md
│   │   ├── site/
│   │   │   ├── index.md
│   │   │   ├── create.md
│   │   │   └── ...
│   │   ├── connector/
│   │   └── ...
│   └── resources/        # 9 resource reference pages
│       ├── index.md
│       ├── site.md
│       ├── connector.md
│       └── ...
└── output/               # Built HTML (optional, for standalone site)
```

**Key Files**:
- `input/commands/*.md` - 43 command pages
- `input/resources/*.md` - 9 resource pages
- Both auto-generated from source, should not be edited manually

### Website MkDocs (website-mkdocs/)

```
website-mkdocs/
├── doc-input/            # Markdown source for website
│   ├── overview/
│   ├── install/
│   ├── kube-cli/         # Existing CLI getting started
│   ├── kube-yaml/        # Existing YAML getting started
│   ├── api-docs/         # Could house reference docs
│   └── index.md
├── mkdocs.yml            # MkDocs configuration
├── config/               # Theme and customization
└── output/               # Built website
```

**Build**: `mkdocs build` or `mkdocs serve`

---

## Integration Options

### Option 1: Copy on Build ❌ (Not Recommended)

**Approach**: Copy generated markdown from refdog to mkdocs during build

```bash
# Build script
cd docs-vale/refdog
./plano generate
cp -r input/commands ../website-mkdocs/doc-input/reference/
cp -r input/resources ../website-mkdocs/doc-input/reference/
cd ../website-mkdocs
mkdocs build
```

**Pros**:
- Simple to understand
- Full control over what's copied

**Cons**:
- ❌ Duplication (files exist in two places)
- ❌ Easy to forget regeneration step
- ❌ Git confusion (which files to commit?)
- ❌ Manual sync required

**Verdict**: Don't use this approach

---

### Option 2: Symlink Integration ✅ (Recommended)

**Approach**: Create symlinks in MkDocs `doc-input/` pointing to refdog `input/`

```bash
cd website-mkdocs/doc-input/
ln -s ../../docs-vale/refdog/input/commands reference/commands
ln -s ../../docs-vale/refdog/input/resources reference/resources
```

**Structure**:
```
website-mkdocs/doc-input/
├── overview/
├── install/
├── reference/              # New directory
│   ├── commands → ../../docs-vale/refdog/input/commands
│   └── resources → ../../docs-vale/refdog/input/resources
└── index.md
```

**Pros**:
- ✅ Single source of truth (refdog input/)
- ✅ No duplication
- ✅ MkDocs reads symlinks automatically
- ✅ Refdog regeneration automatically updates website
- ✅ Clear separation of concerns
- ✅ Can still publish refdog standalone site

**Cons**:
- ⚠️ Symlinks must be relative (for portability)
- ⚠️ Requires both repos cloned together
- ⚠️ Need to configure MkDocs nav manually

**Verdict**: Best approach for maintainability

---

### Option 3: Git Submodule ⚠️ (Overkill)

**Approach**: Make refdog a git submodule of website-mkdocs

**Pros**:
- ✅ Version control for both
- ✅ Official git mechanism

**Cons**:
- ❌ Adds complexity
- ❌ Submodules are notoriously difficult
- ❌ Overkill for local development
- ❌ Still need symlinks or copy

**Verdict**: Not worth the complexity

---

### Option 4: Monorepo ⚠️ (Major Change)

**Approach**: Merge both projects into single repository

**Pros**:
- ✅ Single repo, single build
- ✅ Atomic commits across both

**Cons**:
- ❌ Major restructuring required
- ❌ Breaks existing workflows
- ❌ History complications

**Verdict**: Too disruptive

---

## Recommended Implementation: Option 2 (Symlinks)

### Phase 1: Commands Integration (1 hour)

#### Step 1.1: Create Reference Directory Structure

```bash
cd website-mkdocs/doc-input/
mkdir -p reference
```

#### Step 1.2: Create Symlinks

```bash
cd website-mkdocs/doc-input/reference/
ln -s ../../../docs-vale/refdog/input/commands commands
```

**Verify**:
```bash
ls -la reference/
# Should show: commands -> ../../../docs-vale/refdog/input/commands

ls reference/commands/
# Should show: index.md, site/, connector/, listener/, ...
```

#### Step 1.3: Update MkDocs Configuration

Edit `website-mkdocs/mkdocs.yml`:

```yaml
nav:
  - Home: index.md
  - Overview:
    - Introduction: overview/index.md
    # ... existing nav ...
  
  # NEW: Reference Documentation
  - Reference:
    - Commands: reference/commands/index.md
    - site:
      - Overview: reference/commands/site/index.md
      - create: reference/commands/site/create.md
      - update: reference/commands/site/update.md
      - delete: reference/commands/site/delete.md
      - status: reference/commands/site/status.md
    - connector:
      - Overview: reference/commands/connector/index.md
      - create: reference/commands/connector/create.md
      - update: reference/commands/connector/update.md
      - delete: reference/commands/connector/delete.md
      - status: reference/commands/connector/status.md
    # ... similar structure for listener, link, etc.
```

**Alternative**: Use MkDocs nav generation plugins to auto-discover pages

#### Step 1.4: Test Local Build

```bash
cd website-mkdocs/
mkdocs serve
# Visit http://localhost:8000/reference/commands/
```

**Verify**:
- Commands index loads
- Individual command pages load
- Navigation works
- Styling is correct
- Links work

#### Step 1.5: Regeneration Workflow

```bash
# When Skupper releases new version:
cd docs-vale/refdog/
cp /path/to/skupper/cli-doc/*.md cli-doc/
./plano generate

# Regenerated files automatically appear in website
cd ../../website-mkdocs/
mkdocs serve  # Changes visible immediately
```

---

### Phase 2: Resources Integration (1 hour)

**Prerequisites**: CRD generation implemented in refdog (see SIMPLE-CRD-IMPLEMENTATION.md)

#### Step 2.1: Create Resources Symlink

```bash
cd website-mkdocs/doc-input/reference/
ln -s ../../../docs-vale/refdog/input/resources resources
```

#### Step 2.2: Update MkDocs Navigation

Edit `website-mkdocs/mkdocs.yml`:

```yaml
nav:
  # ... existing nav ...
  
  - Reference:
    - Commands: reference/commands/index.md
    # ... commands nav ...
    
    # NEW: Resources
    - Resources: reference/resources/index.md
    - Site: reference/resources/site.md
    - Connector: reference/resources/connector.md
    - Listener: reference/resources/listener.md
    - Link: reference/resources/link.md
    - AccessGrant: reference/resources/access-grant.md
    - AccessToken: reference/resources/access-token.md
    - RouterAccess: reference/resources/router-access.md
    - AttachedConnector: reference/resources/attached-connector.md
    - AttachedConnectorBinding: reference/resources/attached-connector-binding.md
```

#### Step 2.3: Test and Verify

```bash
mkdocs serve
# Visit http://localhost:8000/reference/resources/
```

---

### Phase 3: Polish and Navigation (1 hour)

#### Step 3.1: Create Reference Landing Page

Create `website-mkdocs/doc-input/reference/index.md`:

```markdown
# Skupper Reference Documentation

Complete reference documentation for Skupper commands and resources.

## Commands

Browse the complete [command reference](commands/index.md) for the Skupper CLI.

**Quick Links**:
- [site commands](commands/site/index.md) - Manage Skupper sites
- [connector commands](commands/connector/index.md) - Expose services
- [listener commands](commands/listener/index.md) - Consume remote services
- [link commands](commands/link/index.md) - Connect sites

## Resources

Browse the complete [resource reference](resources/index.md) for Skupper Kubernetes resources.

**Quick Links**:
- [Site](resources/site.md) - Skupper site configuration
- [Connector](resources/connector.md) - Service exposure
- [Listener](resources/listener.md) - Service consumption
- [Link](resources/link.md) - Site connectivity

## About This Documentation

This reference documentation is automatically generated from:
- **Commands**: Generated from Skupper CLI help text
- **Resources**: Generated from Skupper CRD schemas

This ensures the documentation is always accurate and up-to-date with the actual implementation.
```

#### Step 3.2: Add Cross-Links

Update existing documentation to link to reference:

**In `doc-input/kube-cli/*.md`**:
```markdown
See the complete [command reference](../reference/commands/index.md) for all options.

For detailed information about the `site create` command, see the
[reference documentation](../reference/commands/site/create.md).
```

**In `doc-input/kube-yaml/*.md`**:
```markdown
See the complete [resource reference](../reference/resources/index.md) for all properties.

For detailed information about the Site resource, see the
[reference documentation](../reference/resources/site.md).
```

#### Step 3.3: Add Search Integration

MkDocs search plugin should automatically index reference pages. Verify:

```bash
mkdocs serve
# Search for "site create"
# Search for "linkAccess"
```

#### Step 3.4: Update Home Page

Edit `website-mkdocs/doc-input/index.md`:

```markdown
## Documentation

- **[Getting Started](overview/index.md)** - Introduction to Skupper
- **[Installation](install/index.md)** - Install Skupper
- **[CLI Guide](kube-cli/index.md)** - Using the Skupper CLI
- **[YAML Guide](kube-yaml/index.md)** - Using Skupper with YAML
- **[Reference](reference/index.md)** - Complete command and resource reference  ← NEW
- **[Troubleshooting](troubleshooting/index.md)** - Common issues
```

---

## Build Integration

### Development Workflow

```bash
# Terminal 1: Auto-regenerate refdog docs on changes
cd docs-vale/refdog/
./plano generate --watch  # (if available, otherwise manual)

# Terminal 2: Auto-rebuild website on changes
cd website-mkdocs/
mkdocs serve
```

**Result**: Changes to cli-doc or CRDs automatically flow through to website

### CI/CD Integration

Update `.github/workflows/*.yml` (if exists):

```yaml
name: Build Documentation

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Build refdog reference docs
      - name: Generate refdog documentation
        run: |
          cd docs-vale/refdog
          ./plano generate
      
      # Build MkDocs site
      - name: Build MkDocs
        run: |
          cd website-mkdocs
          pip install -r requirements.txt
          mkdocs build
      
      # Deploy (if on main branch)
      - name: Deploy to GitHub Pages
        if: github.ref == 'main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./website-mkdocs/output
```

### Netlify Integration

If using Netlify, update `netlify.toml`:

```toml
[build]
  publish = "website-mkdocs/output"
  command = """
    cd docs-vale/refdog && ./plano generate && \
    cd ../../website-mkdocs && mkdocs build
  """

[build.environment]
  PYTHON_VERSION = "3.11"
```

---

## MkDocs Compatibility

### Markdown Compatibility

Refdog generates markdown compatible with:
- ✅ MkDocs Material theme
- ✅ Standard markdown
- ✅ GitHub-flavored markdown

**Potential issues**:
- Transom-specific frontmatter (may need stripping)
- Link formats (`.html` vs `/` endings)

**Solution**: Configure MkDocs for compatibility:

```yaml
# mkdocs.yml
use_directory_urls: false  # Use .html links (Transom compatible)
```

### Theme Compatibility

**Material Theme** (recommended):
```yaml
theme:
  name: material
  features:
    - navigation.sections
    - navigation.expand
    - search.suggest
    - content.code.copy
```

**Built-in Themes**: Also work fine with minor style differences

### Plugin Recommendations

```yaml
plugins:
  - search                     # Search integration
  - awesome-pages              # Auto-generate nav from directory structure
  - git-revision-date-localized  # Show last updated dates
```

**awesome-pages** could eliminate manual nav configuration:

```bash
# Install
pip install mkdocs-awesome-pages-plugin

# Enable in mkdocs.yml
plugins:
  - awesome-pages
```

Then MkDocs will auto-discover pages in `reference/commands/` and `reference/resources/`

---

## Migration Strategy

### Incremental Rollout

**Week 1**: Commands only
```bash
# Create commands symlink
ln -s ../../../docs-vale/refdog/input/commands reference/commands
# Update nav, test, deploy
```

**Week 2+**: Add resources (once CRD generation implemented)
```bash
# Create resources symlink
ln -s ../../../docs-vale/refdog/input/resources reference/resources
# Update nav, test, deploy
```

**Week 3**: Polish and cross-links

### Validation Checklist

Before going live:

- [ ] All command pages load correctly
- [ ] All resource pages load correctly
- [ ] Navigation works end-to-end
- [ ] Search finds reference pages
- [ ] Links between pages work
- [ ] Links to external docs work
- [ ] Styling is consistent with rest of site
- [ ] Mobile view works
- [ ] Print view works
- [ ] Reference pages show in site map
- [ ] Regeneration workflow tested
- [ ] CI/CD builds successfully

---

## Alternative: Separate Reference Site

If integration proves difficult, publish refdog as standalone site:

**Option**: Continue using refdog's built-in site generator

```bash
cd docs-vale/refdog/
./plano render  # Build HTML
./plano publish  # Deploy to skupperproject.github.io/refdog
```

**Link from main site**:
```markdown
See the [Skupper Reference Documentation](https://skupperproject.github.io/refdog)
for complete command and resource reference.
```

**Pros**:
- ✅ Completely independent
- ✅ No integration complexity
- ✅ Refdog controls its own styling

**Cons**:
- ❌ Separate navigation
- ❌ Different look and feel
- ❌ Users must navigate between sites

---

## HTML Export Alternative

If MkDocs integration is problematic, export HTML from refdog:

### Option: Generate HTML, Copy to MkDocs Static

```bash
cd docs-vale/refdog/
./plano render  # Generates output/*.html

# Copy to MkDocs static directory
cp -r output/* ../website-mkdocs/docs/static/reference/
```

**Configure MkDocs**:
```yaml
# mkdocs.yml
extra:
  nav:
    - Reference: /static/reference/index.html
```

**Pros**:
- ✅ No markdown compatibility issues
- ✅ Refdog controls styling completely

**Cons**:
- ❌ Separate styling from main site
- ❌ No MkDocs navigation integration
- ❌ Search doesn't index HTML content

**Verdict**: Use only if symlink approach fails

---

## Recommended Timeline

### Phase 1: Commands (Week 1)
- Day 1: Create symlinks, basic nav
- Day 2: Test and verify
- Day 3: Polish and deploy

### Phase 2: Resources (Week 2+)
- Prerequisites: Implement CRD generation in refdog (~3.5 hours)
- Day 1: Add resources symlink
- Day 2: Update nav, test
- Day 3: Deploy

### Phase 3: Enhancement (Week 3)
- Day 1: Add cross-links
- Day 2: Polish reference landing page
- Day 3: Documentation and training

**Total effort**: 2-3 hours integration + 3.5 hours CRD implementation = 6 hours total

---

## Success Criteria

### Must Have
- ✅ Command reference pages accessible from main site nav
- ✅ Resource reference pages accessible from main site nav
- ✅ Search finds reference content
- ✅ Regeneration workflow documented and tested
- ✅ CI/CD builds successfully

### Nice to Have
- ✅ Auto-generated nav (using awesome-pages plugin)
- ✅ Cross-links from guides to reference
- ✅ Last-updated dates on reference pages
- ✅ Print-friendly format

---

## Rollback Plan

If integration causes problems:

```bash
# Remove symlinks
rm website-mkdocs/doc-input/reference/commands
rm website-mkdocs/doc-input/reference/resources

# Revert mkdocs.yml changes
git checkout website-mkdocs/mkdocs.yml

# Rebuild
cd website-mkdocs/
mkdocs build
```

**Refdog continues to work independently** - no harm done!

---

## Questions to Answer

Before starting implementation:

1. **Repository structure**: Are both repos in same parent directory?
   - Current assumption: `repos/sk/vale/docs-vale/` and `repos/sk/vale/website-mkdocs/`
   - Symlinks use relative paths: `../../../docs-vale/refdog/input/`

2. **Build process**: How is website currently built and deployed?
   - Netlify? GitHub Pages? Manual?
   - Need to add refdog generation step

3. **Navigation preference**: Manual nav or auto-generated?
   - Manual: More control, must update for new pages
   - Auto: Less maintenance, less control

4. **MkDocs theme**: Which theme is used?
   - Material recommended (best features)
   - Built-in themes work too

5. **Existing reference docs**: Are there any?
   - Need to migrate or replace?
   - Or is this net-new section?

---

## Next Steps

1. **Verify directory structure**: Confirm repo layout matches assumptions
2. **Choose Phase 1 start date**: When to integrate commands?
3. **Test symlinks locally**: Create symlinks, test `mkdocs serve`
4. **Update mkdocs.yml**: Add reference section to nav
5. **Deploy to staging**: Test before production
6. **Go live**: Merge to main

**Ready to start?** Begin with Phase 1, Step 1.1 above!
