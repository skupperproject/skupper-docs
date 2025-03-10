# Linking sites on local systems using the Skupper CLI

Using the Skupper command-line interface (CLI) allows you to create links between sites.
The link direction is not significant, and is typically determined by ease of connectivity. For example, if east is behind a firewall, linking from east to west is the easiest option.

Once sites are linked, services can be exposed and consumed across the application network without the need to open ports or manage inter-site connectivity.


A *local system* includes Docker, Podman or Linux system.

In this release, the CLI does not support issuing or redeeming tokens.
In this release, the CLI does not support generating `link` resource files.

To link a local system site to a Kubernetes site, see [Linking sites on local systems using YAML](../system-yaml/site-linking.html)