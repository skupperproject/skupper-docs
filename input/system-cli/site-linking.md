<a id="system-linking-cli"></a>
# Linking sites on local systems using the Skupper CLI

Using the Skupper command-line interface (CLI) allows you to create links between sites.
The link direction is not significant, and is typically determined by ease of connectivity. For example, if east is behind a firewall, linking from east to west is the easiest option.

Once sites are linked, services can be exposed and consumed across the application network without the need to open ports or manage inter-site connectivity.


A *local system* includes Docker, Podman or Linux system.

In this release, the CLI does not support issuing tokens.
In this release, the CLI does not support generating `link` resource files.

To link a local system site to a Kubernetes site, you have two options:

* Create a token in a Kubernetes site and follow the instructions below.
* See [Linking sites on local systems using YAML](../system-yaml/site-linking.html)


To create a link by redeeming a token created in a Kubernetes site:

1. Redeem the token on a local system site to create a link:
   ```bash
   skupper token redeem <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

2. Check the status of the link:
   ```bash
   skupper link status
   ```
   You might need to issue the command multiple times before the link is ready:
   ```
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   link-west-skupper-router                        Pending 1       
   ```
   You can now expose services on the application network.
