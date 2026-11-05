<a id="system-linking-cli"></a>
# Linking sites on local systems using the Skupper CLI
<!--ASSEMBLY-->

Use the Skupper CLI on local systems to create links between sites.

Using the Skupper command-line interface (CLI) allows you to create links between sites.
The link direction is not significant, and is typically determined by ease of connectivity. For example, if east is behind a firewall, linking from east to west is the easiest option.

Once sites are linked, services can be exposed and consumed across the application network without the need to open ports or manage inter-site connectivity.

A *local system* includes Docker, Podman or Linux system.

In this release, the CLI does not support issuing tokens for local systems.
However, you can redeem tokens on a local system, and you can create and use 'link' resources.

<a id="system-token-cli"></a>
## Linking to Kubernetes sites using a token
<!--PROCEDURE-->

A token lets a local system site link securely to a Kubernetes site.

A token provides a secure method to link sites.
By default, a token can only be used once and must be used within 15 minutes to link sites.
This procedure describes how to issue a token from a Kubernetes site and redeem that token on a local system site to create a link.

**Prerequisites**

* A local system site and a Kubernetes site.
* A Kubernetes site with `enable-link-access` enabled.

To link sites, you create a token on the Kubernetes site and redeem that token on the local system site to create the link.

There are many options to consider when linking sites using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

**Procedure**

1. On the Kubernetes site where you want to issue the token, make sure link access is enabled:
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

3. Redeem the token on a local system site to create a link:
   ```bash
   skupper token redeem <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

4. Check the status of the link:
   ```bash
   skupper link status
   ```
   You might need to issue the command multiple times before the link is ready:
   ```text
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a       Pending 1       Not Operational
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a       Ready   1       OK
   ```
   You can now expose services on the application network.

<a id="system-link-cli"></a>
## Linking sites using a `link` resource
<!--PROCEDURE-->

An alternative approach to linking sites using tokens is to create a `link` resource YAML file using the CLI, and to apply that resource to another site.

**Prerequisites**

* Two sites
* At least one site with `enable-link-access` enabled.

To link sites, you create a `link` resource YAML file on one site and apply that resource on the other site to create the link.

There are many options to consider when linking sites using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

**Procedure**

1. On the site where you want to create a link , make sure link access is enabled:
   ```bash
   skupper site update --enable-link-access
   skupper site reload
   ```
2. Create a `link` resource YAML file:
   ```bash
   skupper link generate > <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

3. Apply the `link` resource YAML file on a different site to create a link:
   ```bash
   skupper system apply -f <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

4. Check the status of the link:
   ```bash
   skupper link status
   ```
   You might need to issue the command multiple times before the link is ready:
   ```text
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west                                            Pending 1       Not Operational
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west                                            Ready   1       OK
   ```
   You can now expose services on the application network.


   ## Linking a local site through an HTTP proxy[¶](#linking-a-local-site-through-an-http-proxy "Permanent link")

If your network requires routing through an HTTP CONNECT proxy to reach remote sites, you can configure Skupper links on non-Kubernetes (Linux) sites to use a proxy. This feature uses `link` resources with a proxy Secret, allowing the local Skupper router to tunnel inter-site traffic through an HTTP CONNECT proxy.

**Prerequisites**

- A remote site (typically Kubernetes) with `enable-link-access` enabled.
- A local (non-Kubernetes) site installed with `skupper system install`.
- An HTTP CONNECT proxy accessible from the local site.
- Network connectivity from the proxy to the remote site's router endpoints.
- The proxy must allow HTTP CONNECT requests to ports 55671 (inter-router) and 45671 (edge). For example, Squid requires:
    ```
    acl skupper_ports port 55671 45671
    http_access allow CONNECT skupper_ports
    ```

To link a local site through a proxy, you generate a `link` resource YAML from the remote site, create a Secret containing the proxy configuration on the local site, reference the proxy Secret in the link settings, and apply the resources.

**Procedure**

1. On the remote (Kubernetes) site, make sure link access is enabled:
    ```
    skupper site update --enable-link-access
    ```
2. On the remote site, generate a `link` resource YAML file:
    ```
    skupper link generate > link.yaml
    ```
3. Copy the generated `link.yaml` file to the local site.
4. On the local site, create a YAML file for the proxy Secret (for example, `proxy-secret.yaml`):
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

    **📌 NOTE** If your proxy does not require authentication, omit the `username` and `password` fields entirely. The `host` and `port` fields are required.

5. Edit the `link.yaml` file to add the proxy configuration in the `settings` section:
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
    where `my-proxy-config` matches the `metadata.name` of the Secret created in step 4.

6. Place both YAML files into the local site's input resources directory:
    ```
    cp proxy-secret.yaml link.yaml ~/.local/share/skupper/namespaces/<namespace>/input/resources/
    ```
    Replace `<namespace>` with the namespace of your local site (typically `default`). If running as root, use `/var/lib/skupper/namespaces/<namespace>/input/resources/` instead.

7. Reload the site configuration to apply the changes:
    ```
    skupper system reload <namespace>
    ```
8. Check the status of the link:
    ```
    skupper link status
    ```
    You might need to issue the command multiple times before the link is ready.

**How it works**

When the system controller processes the link, it:

- Reads the proxy Secret to extract `host`, `port`, and optional `username`/`password`.
- Writes the password to a secure file under `runtime/proxies/<secret-name>/password.txt` (mode 0600).
- Configures a `proxyProfile` on the Skupper router connector, which routes the AMQP-over-TLS connection through an HTTP CONNECT tunnel to the remote site.

All inter-site traffic remains protected by mutual TLS inside the proxy tunnel.

**Troubleshooting**

If the link remains in "Pending" or "Not Operational" status, check:

- The proxy Secret exists and contains the correct `host` and `port` values.
- The proxy is accessible from the local site.
- If using authentication, both `username` and `password` must be present. A `username` without a `password` is ignored with a warning.
- The Secret type must be `kubernetes.io/basic-auth`. Other types are ignored with a warning.
- Router logs for connection errors:
    ```
    journalctl -u skupper-<namespace>.service
    ```
- Validate resources before applying:
    ```
    skupper system validate <namespace>
    ```

**📌 NOTE** If you update the proxy Secret after the link is established, reload the site configuration to apply the changes:

```
skupper system reload <namespace>
```

There are many options to consider when linking sites using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

