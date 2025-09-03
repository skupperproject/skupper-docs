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

2. Install the controller for Podman and Docker sites:

   ```bash
   skupper system install
   ```
   This runs a container to support site, link and service operations.
   This feature is not available on Linux local system sites (systemd).

3. Create a site:

   ```bash
   skupper site create <site-name>
   ```
   For example:
   ```bash
   skupper site create my-site
   
   Waiting for status...
   Site "my-site" is ready.
   ```
   While the site is created, the site is not running at this point.
   To run the site:
   ```bash
   skupper system start
   ```

By default, all sites are created with the namespace `default`.
On non-Kubernetes sites, you can create multiple sites per-user by specifying a *namespace*, for example you can create multiple sites with different platforms as follows:

```bash
skupper site create systemd-site -p linux -n linux-ns
skupper site create docker-site -p docker -n docker-ns
```


<a id="system-deleting-site-cli"></a>
## Deleting a site using the CLI on local systems

**Prerequisites**

* The `skupper` CLI is installed.

**Procedure**

1. Enter the following command to delete a site:
   ```bash
   skupper site delete <sitename>
   skupper system stop
   ```

2. You can also uninstall the controller after deleting all existing sites:
   ```bash
   skupper system uninstall
   ```

<a id="system-creating-site-bundle"></a>
## Creating a site bundle using the CLI on local systems

Sometimes, you might want to create all the configuration for a site and apply it automatically to a remote host.
To support this, Skupper allows you create a `.tar.gz` file with all the required files and an `install.sh` script to start the remote site.


**Prerequisites**

* The `skupper` CLI is installed. The CLI is not required on the remote site.

**Procedure**

1. Set the `SKUPPER_PLATFORM` for type of site you want to install:

   * `podman`
   * `docker`
   * `linux`

2. Install the controller for Podman and Docker sites:

   ```bash
   skupper system install
   ```
   This runs a container to support site, link and service operations.
   This feature is not available on Linux local system sites (systemd).

3. Create a site:

   ```bash
   skupper site create <site-name>
   ```
   For example:
   ```bash
   skupper site create remote-site
   
   Waiting for status...
   Site "remote-site" is ready.
   ```
   While the site is created, the site is not running and that is not a requirement for this usecase.

4. Create the bundle:
   ```bash
    skupper system generate-bundle remote-site
   ```
   The output shows the location of the generated `.tar.gz` file, for example:
   ```
   Site "remote-site" has been created (as a distributable bundle)
   Installation bundle available at: /home/user/.local/share/skupper/bundles/remote-site.tar.gz
   Default namespace: default
   Default platform: podman
   ```
5. Transfer the bundle file to the remote location and uncompress the file in an appropriate location:
   ```bash
   tar -xzvf remote-site.tar.gz
   ```

6. Start the site:
   ```bash
   install.sh
   ```
   The site is now running, you can verify with `skupper site status` if the CLI is installed at that location.


[cli-ref]: https://skupperproject.github.io/refdog/commands/index.html
