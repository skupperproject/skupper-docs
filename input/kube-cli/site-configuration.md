<a id="kube-creating-site-cli"></a>
# Creating a site on Kubernetes using the Skupper CLI

Using the skupper command-line interface (CLI) allows you to create and manage sites from the context of the current namespace.

A typical workflow is to create a site, link sites together, and expose services to the application network.

<a id="kube-checking-cli"></a>
## Checking the Skupper CLI

Installing the skupper command-line interface (CLI) provides a simple method to get started with Skupper.

1. Follow the instructions for [Installing Skupper](https://skupper.io/releases/index.html).

2. Verify the installation.
   ```bash
   skupper version
   
   COMPONENT               VERSION
   cli                     {{skupper_cli_version}}
   ```

<a id="kube-creating-simple-site-cli"></a>
## Creating a simple site using the CLI on Kubernetes

**Prerequisites**

* The `skupper` CLI is installed.
* The Skupper controller is running on the Kubernetes cluster you are running or you are running on a platform.

**Procedure**

1. Check that the `SKUPPER_PLATFORM` environment is unset or set to `kubernetes`.

   * `kubernetes` - default
   * `podman`
   * `docker`
   * `linux`

2. Create a site on Kubernetes:

   ```bash
   skupper site create <site-name> --namespace <namespace>
   ```
   Specifying the namespace is not required if the context is set to the namespace where you want to create the site.
   For example:
   ```bash
   skupper site create my-site
   
   Waiting for status...
   Site "my-site" is ready.
   ```
There are many options to consider when creating sites using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

For example

* `--enable-link-access`
  
  If enabled, this option allows you create tokens and link *to* this site.
  By default, this option is disabled but you can change the setting later `skupper site update --enable-link-access`.

* `--timeout <time>`

  You can add the timeout option to specify the maximum time for the CLI wait for the site status to report `ready`.
  ```
  skupper site create my-site --timeout 2m
  ```
  The timeout option does not stop the site from being created, but if the site is not ready, the following is output:
  
  ```
  Site "my-site" is not yet ready: Pending
  ```
  You can check the status of the site at any time using `skupper site status`.

<a id="kube-deleting-site-cli"></a>
## Deleting a site using the CLI on Kubernetes

**Prerequisites**

* The `skupper` CLI is installed.

**Procedure**

1. Change context to the namespace where the site was created, for example:
   ```bash
   kubectl config set-context --current --namespace west
   ```

2. Enter the following command to delete a site:
   ```bash
   skupper site delete
   ```
[cli-ref]: https://skupperproject.github.io/refdog/commands/index.html
