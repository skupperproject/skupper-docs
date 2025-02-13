# Using the Skupper CLI

Using the skupper command-line interface (CLI) allows you to create and manage Skupper sites from the context of the current namespace.

A typical workflow is to create a site, link sites together, and expose services to the service network.

## Checking the Skupper CLI

Installing the skupper command-line interface (CLI) provides a simple method to get started with Skupper.

1. Follow the instructions for [Installing Skupper](https://skupper.io/releases/index.html).

2. Verify the installation.
   ```bash
   $  skupper version
   COMPONENT               VERSION
   router                  3.1.0
   controller              2.0.0-preview-2
   network-observer        2.0.0-preview-2
   cli                     2.0.0-preview-2
   prometheus              v2.42.0
   origin-oauth-proxy      4.14.0
   ```

## Creating a simple site using the CLI

**Prerequisites**

* The `skupper` CLI is installed.
* The Skupper controller is running on the Kubernetes cluster you are running or you are running on a platform.

1. Set the `SKUPPER_PLATFORM` for your site if you are not using Kubernetes/OpenShift:

   * `kubernetes` - default
   * `podman`
   * `docker`

2. Create a site:

   ```bash
   $ skupper site create <site-name>
   ```

   On Kubernetes, the site is created automatically.
   However, on other platforms this process creates the YAML file defining the site.

   ```bash
   $ skupper site create site-a
   File written to /home/paulwright/.local/share/skupper/namespaces/default/input/resources/sites/site-a.yaml
   ```

   To make the site active on non-Kubernetes sites:

   ```bash
   $ skupper system setup
   ```


## Advanced site creation


  📌 NOTE: On non-Kubernetes sites, you can create multiple sites per-user by specifying a *namespace*.
  