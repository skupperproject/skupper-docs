# Creating a site on Kubernetes using the Skupper CLI

Using the skupper command-line interface (CLI) allows you to create and manage Skupper sites from the context of the current namespace.

A typical workflow is to create a site, link sites together, and expose services to the service network.

## Checking the Skupper CLI

Installing the skupper command-line interface (CLI) provides a simple method to get started with Skupper.

1. Follow the instructions for [Installing Skupper](https://skupper.io/releases/index.html).

2. Verify the installation.
   ```bash
   $  skupper version
   COMPONENT               VERSION
   router                  3.2.0
   controller              2.0.0-rc1
   network-observer        2.0.0-rc1
   cli                     2.0.0-rc1
   prometheus              v3.0.1
   origin-oauth-proxy      4.14.0
   ```

## Creating a simple site using the CLI on Kubernetes

**Prerequisites**

* The `skupper` CLI is installed.
* The Skupper controller is running on the Kubernetes cluster you are running or you are running on a platform.

.Procedure

1. Check that the `SKUPPER_PLATFORM` environment is unset or set to `kubernetes`.

   * `kubernetes` - default
   * `podman`
   * `docker`
   * `linux`

2. Create a site on Kubernetes:

   ```bash
   $ skupper site create <site-name>
   ```
   For example:
   ```bash
   $ skupper site create my-site
   Waiting for status...
   Site "my-site" is ready.
   ```

## Creating a simple site using YAML on Kubernetes

**Prerequisites**

* The Skupper controller is running on the Kubernetes cluster you are running or you are running on a platform.

.Procedure

1. Create a site CR yaml file, for example
