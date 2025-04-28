<a id="system-creating-site-cli"></a>
# Creating a site on a local system using the Skupper CLI

Using the skupper command-line interface (CLI) allows you to create and manage Skupper sites from the context of the current user.

A typical workflow is to create a site, link sites together, and expose services to the application network.

A *local system* includes Docker, Podman or Linux system.

If you require more than one site, specify a unique namespace when using  `skupper`, for example `skupper --namespace second-site ...`.


<a id="system-checking-cli"></a>
## Checking the Skupper CLI and environment

Installing the skupper command-line interface (CLI) provides a simple method to get started with Skupper.

1. Follow the instructions for [Installing Skupper](https://skupper.io/releases/index.html).

2. Verify the installation.
   ```bash
   skupper version
   
   COMPONENT               VERSION
   cli                     {{skupper_cli_version}}
   ```

3. For podman sites:

   Make sure the Podman socket is available. To enable it:
   ```bash
   systemctl --user enable --now podman.socket
   ```
   Enable lingering to ensure the site persists over logouts:
   ```bash
   loginctl enable-linger <username>
   ```

<a id="system-creating-simple-site-cli"></a>
## Creating a simple site using the CLI on local systems

**Prerequisites**

* The `skupper` CLI is installed.

**Procedure**

1. Set the `SKUPPER_PLATFORM` for type of site you want to install:

   * `podman`
   * `docker`
   * `linux`

2. Create a site:

   ```bash
   skupper site create <site-name>
   ```
   For example:
   ```bash
   skupper site create my-site
   
   Waiting for status...
   Site "my-site" is ready.
   ```

  📌 NOTE: On non-Kubernetes sites, you can create multiple sites per-user by specifying a *namespace*.

<a id="system-deleting-site-cli"></a>
## Deleting a site using the CLI on local systems

**Prerequisites**

* The `skupper` CLI is installed.

**Procedure**

1. Enter the following command to delete a site:
   ```bash
   skupper system teardown
   ```

[cli-ref]: https://skupperproject.github.io/refdog/commands/index.html
