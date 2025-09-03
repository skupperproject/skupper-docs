<a id="system-linking-cli"></a>
# Linking sites on local systems using the Skupper CLI

Using the Skupper command-line interface (CLI) allows you to create links between sites.
The link direction is not significant, and is typically determined by ease of connectivity. For example, if east is behind a firewall, linking from east to west is the easiest option.

Once sites are linked, services can be exposed and consumed across the application network without the need to open ports or manage inter-site connectivity.

A *local system* includes Docker, Podman or Linux system.

In this release, the CLI does not support issuing tokens for local systems.
However, you can redeem tokens on a local system, and you can create and use 'link' resources.

<a id="system-token-cli"></a>
## Linking to Kubernetes sites using a token

A token provides a secure method to link sites.
By default, a token can only be used once and must be used within 15 minutes to link sites.
This procedure describes how to issue a token from a Kubernetes site and redeem that token on a local system site to create a link.

**Prerequisites**

* A local system site and a Kubernetes site.
* A Kubernetes site with `enable-link-access` enabled.

To link sites, you create a token on the Kubernetes site and redeem that token on the local system site to create the link.

**Procedure**

1. On the Kubernetes site where you want to issue the token, make sure link access is enabled:
   ```bash
   skupper site update --enable-link-access
   ```
2. Create a token:
   ```bash
   skupper token issue <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

   This file contains a key and the location of the site that created it.
   
   **📌 NOTE**
   Access to this file provides access to the application network. 
   Protect it appropriately.
   A token can be restricted by any combination of:

   * Time - prevents token reuse after a specified period.
     
     For example, to allow a token to be used for 1 hour after it is issued:
     ```
     skupper token issue build/west.yaml --expiration-window 60m
     ```
   * Usage - prevents creating multiple links from a single token.
     
     For example, to allow a token to be used 3 times:
     ```
     skupper token issue output/west.yaml --redemptions-allowed 3
     ```
   
   All inter-site traffic is protected by mutual TLS using a private, dedicated certificate authority (CA).
   A token is not a certificate, but is securely exchanged for a certificate during the linking process.

3. Redeem the token on a local system site to create a link:
   ```bash
   skupper token redeem <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

4. Check the status of the link:
   ```bash
   skupper link status
   ```
   You might need to issue the command multiple times before the link is ready:
   ```
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a       Pending 1       Not Operational
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a       Ready   1       OK
   ```
   You can now expose services on the application network.

There are many options to consider when linking sites using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

<a id="kube-link-cli"></a>
## Linking sites using a `link` resource

An alternative approach to linking sites using tokens is to create a `link` resource YAML file using the CLI, and to apply that resource to another site.

**Prerequisites**

* Two sites
* At least one site with `enable-link-access` enabled.

To link sites, you create a `link` resource YAML file on one site and apply that resource on the other site to create the link.

**Procedure**

1. On the site where you want to create a link , make sure link access is enabled:
   ```bash
   skupper site update --enable-link-access
   skupper site reload
   ```
2. Create a `link` resource YAML file:
   ```bash
   skupper link generate > <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

3. Apply the `link` resource YAML file on a different site to create a link:
   ```bash
   skupper system apply -f <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

4. Check the status of the link:
   ```bash
   skupper link status
   ```
   You might need to issue the command multiple times before the link is ready:
   ```
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west                                            Pending 1       Not Operational
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west                                            Ready   1       OK
   ```
   You can now expose services on the application network.

There are many options to consider when linking sites using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

