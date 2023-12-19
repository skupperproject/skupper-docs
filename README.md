# Skupper documentation repo

This repo contains the user documentation for https://skupper.io.


```bash
/cli # Skupper CLI usage
/console # Skupper console usage
/declarative # YAML instructions
/kubernetes # Running Skupper in a cluster
/podman # Running Skupper on Linux
/operator # Kubernetes with operators
/overview # Introduction to Skupper
/policy # Kubernetes Skuper policies
/troubleshooting # Help when you are encountering issues

```

## Contributing to the documentation

Skupper welcomes contributions from the community. To contribute to the documentation.

To file a documentation bug or tell us about any other issue with the documentation, create an issue at [skupperproject/skupper-docs](https://github.com/skupperproject/skupper-docs/issues).

## Building the documentation

You must have the following tools to build the documentation:

* link:https://github.com/asciidoctor/asciidoctor[`asciidoctor` (1.5.6)] for building books

Clone the skupper-docs repository:

```bash
$ git clone https://github.com/skupperproject/skupper-docs.git
$ cd skupper-docs
```
Build the documentation:

```bash
$ make build
```