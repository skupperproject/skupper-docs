<a id="system-yaml-site-linking"></a>
# Link sites on local systems using YAML
<!--ASSEMBLY-->

Use a `link` resource YAML file to create links between local system and Kubernetes sites.

Using a `link` resource YAML file allows you to create links between sites.
The link direction is not significant, and is typically determined by ease of connectivity. For example, if east is behind a firewall, linking from east to west is the easiest option.

Once sites are linked, services can be exposed and consumed across the application network without the need to open ports or manage inter-site connectivity.

The procedures below describe linking an existing site.
Typically, it is easier to configure a site, links, and services in a set of files.
Create a configured site by applying all the YAML files using `skupper system apply`.

<a id="system-link-yaml"></a>
## Link sites using a `link` resource and YAML
<!--PROCEDURE-->

Create a `link` resource YAML file and apply it to the local system site to establish a link.

An alternative approach to linking sites using tokens is to create a `link` resource YAML file, and to apply that resource to the local system site.

**Prerequisites**

* A local system site
* A Kubernetes site with `enable-link-access` enabled.

To link sites, you create a `link` resource YAML file on one site and apply that resource on the other site to create the link.

**Procedure**

1. On the site where you want to create a link , ensure link access is enabled:
   ```bash
   skupper site update --enable-link-access
   ```
2. Create a `link` resource YAML file:
   ```bash
   skupper link generate > <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

3. Apply the `link` resource YAML file on a local system site to create a link:
   ```bash
   skupper system apply -f <filename>.yaml
   skupper system reload
   ```
   where `<filename>.yaml` is the name of the YAML file saved on your local filesystem.
   The file must have a `.yaml` or `.json` extension.

   The `apply` command stages the resource into `~/.local/share/skupper/namespaces/<namespace>/input/resources/`.
   The `reload` command processes the staged resources and establishes the link.
   The path is specific to the namespace; if you are configuring a different namespace, use that name instead.

4. Check the status of the link:
   ```bash
   skupper link status
   ```
   The output shows the link name:
   ```text
   $ skupper link status
   NAME            STATUS
   link-west       Ok
   ```
   You can now expose services on the application network.
