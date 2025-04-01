<a id="system-yaml-site-configuration"></a>
# Creating a site on local systems using YAML

Using YAML allows you to create and manage sites on Docker, Podman and Linux.

A typical workflow is to create a site, link sites together, and expose services to the application network.

If you require more than one site, specify a unique namespace when using  `skupper`, for example `skupper --namespace second-site ...`.

<a id="system-creating-simple-site-yaml"></a>
## Creating a simple site on local systems using YAML

You can use YAML to create and manage Skupper sites.

**Prerequisites**

* The `skupper` CLI is installed.


**Procedure**

1. Create a site CR YAML file named `my-site.yaml` in an empty directory, for example, `local`:

   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: Site
   metadata:
     name: my-site
   ```
   This YAML creates a site named `my-site` in the `default` namespace.

2. Create the site:
   ```bash
   skupper system setup --path ./local
   ```
   Skupper attempts to process any files in the `local` directory.
   Typically, you create all resources you require for a site before running `skupper system setup`.

3. Check the status of the site:
   ```bash
   skupper site status
   ```
   You might need to issue the command multiple times before the site is ready:
   ```
   NAME    STATUS  MESSAGE
   default Ready   OK
   ```
   You can now link this site to another site to create an application network.

There are many options to consider when creating sites using YAML, see [YAML Reference][yaml-ref], including *frequently used* options.

[yaml-ref]: https://skupperproject.github.io/refdog/resources/index.html