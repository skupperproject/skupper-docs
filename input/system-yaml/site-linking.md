<a id="system-yaml-site-linking"></a>
# Linking sites on local systems using YAML


Using a `link` resource YAML file allows you to create links between sites.
The link direction is not significant, and is typically determined by ease of connectivity. For example, if east is behind a firewall, linking from east to west is the easiest option.

Once sites are linked, services can be exposed and consumed across the application network without the need to open ports or manage inter-site connectivity.

The procedures below describe linking an existing site.
Typically, it is easier to configure a site, links and services in a set of files and then create a configured site by placing all the YAML files in a directory, for example `local` and then using the following command to 

<a id="system-link-yaml"></a>
## Linking sites using a `link` resource

An alternative approach to linking sites using tokens is to create a `link` resource YAML file using the CLI, and to apply that resource to another site.

**Prerequisites**

* A local system site
* A Kubernetes site with `enable-link-access` enabled.

To link sites, you create a `link` resource YAML file on one site and apply that resource on the other site to create the link.

**Procedure**

1. On the site where you want to create a link , make sure link access is enabled:
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
   mv <filename> ~/.local/share/skupper/namespaces/default/input/resources/
   skupper system setup --force
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

   The path shown is specific to the `default` namespace.
   If you are configuring a different namespace, use that name instead.

   The site is recreated and you see some of the internal resources that are not affected, for example:
   ```
   Sources will be consumed from namespace "default"
   2025/03/09 22:43:14 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-local-ca/tls.crt
   2025/03/09 22:43:14 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-local-ca/tls.key
   2025/03/09 22:43:14 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-local-ca/ca.crt
   2025/03/09 22:43:14 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-site-ca/tls.crt
   2025/03/09 22:43:14 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-site-ca/tls.key
   2025/03/09 22:43:14 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-site-ca/ca.crt
   2025/03/09 22:43:15 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-service-ca/tls.crt
   2025/03/09 22:43:15 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-service-ca/tls.key
   2025/03/09 22:43:15 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-service-ca/ca.crt
   
   ```

4. Check the status of the link:
   ```bash
   skupper link status
   ```
   The output shows the link name:
   ```
   $ skupper link status
   NAME            STATUS
   link-west       Ok
   ```
   You can now expose services on the application network.
