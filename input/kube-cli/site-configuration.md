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
   cli                     {{skupper_cli_version}}
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
There are many options to consider when creating sites using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.


## Creating a simple site using YAML on Kubernetes

You can use YAML to create and manage Skupper sites.

**Prerequisites**

* The Skupper controller is running on the Kubernetes cluster you are running or you are running on a platform.

.Procedure

1. Create a site CR YAML file named `my-site.yaml`, for example:

   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: Site
   metadata:
     name: my-site
   ```
   This YAML creates a site named `my-site` in the current namespace.

2. Create the site:
   ```bash
   kubectl apply -f my-site.yaml
   ```

3. Check the status of the site:
   ```bash
   kubectl get site
   ```
   You might need to issue the command multiple times before the site is ready:
   ```
   $ kubectl get site
   NAME   STATUS    SITES IN NETWORK   MESSAGE
   west   Pending                      containers with unready status: [router kube-adaptor]
   $ kubectl get site
   NAME   STATUS   SITES IN NETWORK   MESSAGE
   west   Ready    1                  OK
   ```
   You can now link this site to another site to create an application network.

There are many options to consider when creating sites using YAML, see [YAML Reference][yaml-ref], including *frequently used* options.

[cli-ref]: https://skupperproject.github.io/refdog/commands/index.html
[yaml-ref]: https://skupperproject.github.io/refdog/resources/index.html