# Refdog: Skupper Reference Doc Generation

This repo area contains the refdog generator plus the MkDocs content that consumes its output.

## Start here

The canonical user workflow now lives in [refdog/README.md](./refdog/README.md).

That README explains:

- what users should edit
- where markdown is generated
- how `docs-vale/refdog/input/` relates to `docs-vale/input/refdog/`
- how to run refdog
- how to build MkDocs

## Short version

Refdog generates reference markdown from source material:

- commands from `refdog/cli-doc/*.md`
- resources from `refdog/config/resources/*.yaml`, with CRDs available in `refdog/crds/`

The generated files are written to:

- `docs-vale/refdog/input/`

MkDocs does not build from that tree directly. MkDocs reads from:

- `docs-vale/input/`

So the current workflow is:

```bash
cd docs-vale/refdog
./plano generate

cd ..
rsync -a refdog/input/ input/refdog/
mkdocs build
```

## Additional reference

These documents remain for deeper technical background:

- [refdog/resources.md](./refdog/resources.md)
- [refdog/crd-generation-proposal.md](./refdog/crd-generation-proposal.md)
