# Refdog

Refdog generates the Skupper reference markdown that later gets built into the MkDocs site.

## What this directory is for

`refdog/` is the generation workspace.

- `cli-doc/`: command source markdown copied from the Skupper CLI repo
- `crds/`: CRD YAML copied from the Skupper repo
- `config/`: refdog configuration and overview text
- `python/`: generator code
- `input/`: generated refdog markdown

The generated output here is not the final website. MkDocs builds from `input/`.

## Pipeline

The current pipeline is:

1. Update command source files in `cli-doc/`.
2. Optionally update CRDs in `crds/`.
3. Run refdog generation.
4. Make sure the generated markdown under `refdog/input/` is mirrored into `../input/refdog/`.
5. Run MkDocs from `` or the website build from `website-mkdocs/`.

The important distinction is:

- Refdog generates markdown in `refdog/input/`
- MkDocs reads markdown from `input/`
- Final HTML ends up under `output/docs/` for the `docs-vale` build or `website-mkdocs/output/docs/` for the website build

## What actually generates markdown

Run this from `refdog/`:

```bash
./plano generate
```

That command is defined in `.plano.py` and calls the Python generators under `python/`.

Key files:

- `python/generate.py`: orchestration
- `python/commands.py`: generates `input/commands/*.md`
- `python/resources.py`: generates `input/resources/*.md`
- `python/concepts.py`: generates `input/concepts/*.md`

For example, `config/commands/overview.md` is appended into the generated command index.

## Current source of truth

### Commands

Commands are generated from `cli-doc/*.md`.

This path is active now and is the main thing users should maintain for releases.

### Resources

Resource pages are also generated today, but the resource model still depends on `config/resources/*.yaml` for most of the authored content. The CRDs are loaded for checking and schema lookups, but this is not a pure CRD-driven pipeline yet.

## Normal user workflow

From `refdog/`:

```bash
# 1. Update source files
cp /path/to/skupper/cli-doc/*.md cli-doc/
# Optional if resource source changed
cp /path/to/skupper/crds/*.yaml crds/

# 2. Regenerate refdog markdown
./plano generate
```

From ``:

```bash
# 3. Mirror refdog output into the MkDocs input tree
rsync -a refdog/input/ input/refdog/

# 4. Build the docs site
mkdocs build
```

If you want the helper wrapper:

```bash
./regenerate-refdog.sh
```

That script runs `refdog/./plano generate` using the fixed `/docs/refdog` mount path.

## Build commands

### Rebuild only refdog markdown

```bash
cd refdog
./plano generate
```

### Rebuild MkDocs docs

```bash
cd docs-vale
mkdocs build
```

### Rebuild the website variant

```bash
cd website-mkdocs
./build.sh
```

## What the user should edit

Edit these:

- `cli-doc/*.md` when updating command reference source from Skupper
- `crds/*.yaml` when updating CRD source from Skupper
- `config/commands/overview.md` and other `config/*/overview.md` files for section intro text
- generator code under `python/` when changing how pages are produced

Avoid editing these directly:

- `input/**/*.md` under `refdog/`
- `input/refdog/**/*.md`
- built HTML under `output/` or `website-mkdocs/output/`

Those are generated artifacts.

## Current caveat

There is no clear checked-in automation in this repo that copies `refdog/input/` into `input/refdog/` as part of the build. In practice, the MkDocs tree currently contains a mirrored copy, but the handoff is still a separate step and should be treated that way.

If this repo is going to be maintained long-term, that handoff should either be automated in the build or replaced with a symlink-based arrangement.

## Optional background docs

These are retained as deeper reference, not as the primary workflow:

- `resources.md`
- `crd-generation-proposal.md`
