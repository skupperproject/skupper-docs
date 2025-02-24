# Creating a site on Linux using the Skupper CLI

Using the skupper command-line interface (CLI) allows you to create and manage Skupper sites from the context of the current user.

A typical workflow is to create a site, link sites together, and expose services to the service network.

## Checking the Skupper CLI and environment

Installing the skupper command-line interface (CLI) provides a simple method to get started with Skupper.

1. Follow the instructions for [Installing Skupper](https://skupper.io/releases/index.html).

2. Verify the installation.
   ```bash
   skupper version
   
   COMPONENT               VERSION
   router                  3.2.0
   controller              2.0.0-rc1
   network-observer        2.0.0-rc1
   cli                     2.0.0-rc1
   prometheus              v3.0.1
   origin-oauth-proxy      4.14.0
   ```
3. For podman sites, the Podman socket must be available. To enable it:
   ```bash
   systemctl --user enable --now podman.socket
   ```

## Creating a simple site using the CLI on Linux

**Prerequisites**

* The `skupper` CLI is installed.

.Procedure

1. Set the `SKUPPER_PLATFORM` for type of site you want to install:

   * `podman`
   * `docker`
   * `linux`

2. Create a site on Kubernetes/OpenShift:

   ```bash
   $ skupper site create <site-name>
   ```
   For example:
   ```bash
   $ skupper site create my-site
   Waiting for status...
   Site "my-site" is ready.
   ```

  📌 NOTE: On non-Kubernetes sites, you can create multiple sites per-user by specifying a *namespace*.
