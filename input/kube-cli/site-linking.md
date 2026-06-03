<a id="kube-linking-cli"></a>
# Linking sites on Kubernetes using the Skupper CLI
<!--ASSEMBLY-->

Create links between sites on Kubernetes by using the CLI.

Using the Skupper command-line interface (CLI) allows you to create links between sites.
The link direction is not significant, and is typically determined by ease of connectivity. For example, if east is behind a firewall, linking from east to west is the easiest option.

Once sites are linked, services can be exposed and consumed across the application network without the need to open ports or manage inter-site connectivity.

<a id="kube-token-cli"></a>
## Linking sites using a token
<!--PROCEDURE-->

A token provides a secure method to link sites.
By default, a token can only be used once and must be used within 15 minutes to link sites.
This procedure describes how to issue a token from one site and redeem that token on another site to create a link.

**Prerequisites**

* Two sites
* At least one site with `enable-link-access` enabled.

To link sites, you create a token on one site and redeem that token on the other site to create the link.

**Procedure**

1. On the site where you want to issue the token, make sure link access is enabled:
   ```bash
   skupper site update --enable-link-access
   ```
2. Create a token:
   ```bash
   skupper token issue <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

   This file contains a key and the location of the site that created it.
   
   **📌 NOTE**
   Access to this file provides access to the application network. 
   Protect it appropriately.
   A token can be restricted by any combination of:

   * Time - prevents token reuse after a specified period.
     
     For example, to allow a token to be used for 1 hour after it is issued:
     ```
     skupper token issue build/west.yaml --expiration-window 60m
     ```
   * Usage - prevents creating multiple links from a single token.
     
     For example, to allow a token to be used 3 times:
     ```
     skupper token issue output/west.yaml --redemptions-allowed 3
     ```
   
   All inter-site traffic is protected by mutual TLS using a private, dedicated certificate authority (CA).
   A token is not a certificate, but is securely exchanged for a certificate during the linking process.

3. Redeem the token on a different site to create a link:
   ```bash
   skupper token redeem <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

4. Check the status of the link:
   ```bash
   skupper link status
   ```
   You might need to issue the command multiple times before the link is ready:

   ```bash
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a       Pending 1       Not Operational
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a       Ready   1       OK
   ```
   You can now expose services on the application network.

There are many options to consider when linking sites using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

<a id="kube-link-cli"></a>
## Linking sites using a `link` resource
<!--PROCEDURE-->

An alternative approach to linking sites using tokens is to create a `link` resource YAML file using the CLI, and to apply that resource to another site.

**Prerequisites**

* Two sites
* At least one site with `enable-link-access` enabled.

To link sites, you create a `link` resource YAML file on one site and apply that resource on the other site to create the link.

**Procedure**

1. On the site where you want to create a link, make sure link access is enabled:
   ```bash
   skupper site update --enable-link-access
   ```
2. Create a `link` resource YAML file:
   ```bash
   skupper link generate > <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.
   The `link` YAML file contains the following information:
   * The name of the link
   * The certificate used to authenticate the link
   * Two host and port entries for the listening site are included for each link.
   
   If the listening site uses high availability mode, two link resources are created.

3. Apply the `link` resource YAML file on a different site to create a link:
   ```bash
   kubectl apply -f <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

4. Check the status of the link:
   ```bash
   skupper link status
   ```
   You might need to issue the command multiple times before the link is ready:

   ```bash
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a       Pending 1       Not Operational
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a       Ready   1       OK
   ```
   You can now expose services on the application network.

There are many options to consider when linking sites using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

<a id="kube-proxy-cli"></a>
## Linking sites through an HTTP proxy
<!--PROCEDURE-->

If your network requires routing through an HTTP CONNECT proxy to reach remote sites, you can configure Skupper links to use a proxy.
This feature is only available when using `link` resources, not tokens.

**Prerequisites**

* Two sites
* At least one site with `enable-link-access` enabled.
* An HTTP CONNECT proxy accessible from the linking site
* Network connectivity from the proxy to the listening site's router endpoints
* The proxy must allow HTTP CONNECT requests to ports 55671 (inter-router) and 45671 (edge). For example, Squid requires:
  ```
  acl skupper_ports port 55671 45671  
  http_access allow CONNECT skupper_ports
  ```

To link sites through a proxy, you create a Secret containing the proxy configuration, generate a `link` resource YAML file, reference the proxy Secret in the link settings, and apply that resource to create the link.

**Procedure**

1. On the listening site, make sure link access is enabled:
   ```bash
   skupper site update --enable-link-access
   ```

2. On the listening site, create a `link` resource YAML file:
   ```bash
   skupper link generate > link.yaml
   ```

3. Copy the generated `link.yaml` file to the linking site.

4. On the linking site, create a Secret with the proxy configuration:
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: my-proxy-config
   type: kubernetes.io/basic-auth
   stringData:
     host: proxy.example.com
     port: "3128"
     username: myuser
     password: mypassword
   ```
  
   **📌 NOTE**
   If your proxy does not require authentication, remove the username and password.
 
5. On the linking site, edit the `link.yaml` file to add the proxy configuration in the settings section:
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: Link
   metadata:
     name: link-to-remote-site
   spec:
     cost: 1
     endpoints:
     - host: remote-site.example.com
       name: inter-router
       port: "55671"
     - host: remote-site.example.com
       name: edge
       port: "45671"
     tlsCredentials: link-to-remote-site
     settings:
       proxy-configuration: my-proxy-config
   ```
   where `my-proxy-config` is the name of the Secret created in step 4.

6. On the linking site, apply the `link` resource YAML file to create the link:
   ```bash
   kubectl apply -f link.yaml
   ```

7. Check the status of the link:
   ```bash
   skupper link status
   ```
   You might need to issue the command multiple times before the link is ready.
   
   If the link remains in "Pending" or "Not Operational" status, check:
   
   * The proxy Secret exists and contains the correct host and port
   * The proxy is accessible from the router pod
   * Router logs for connection errors: `kubectl logs deployment/skupper-router`

   **📌 NOTE**
   If you update the proxy Secret, you must trigger a reconciliation to apply the changes:
   ```bash
   kubectl annotate link <link-name> reconcile=$(date +%s) --overwrite
   ```

All inter-site traffic is protected by mutual TLS and routed through the HTTP CONNECT proxy tunnel.
You can now expose services on the application network.

There are many options to consider when linking sites using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.
