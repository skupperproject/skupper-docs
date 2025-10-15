<a id="kube-yaml-site-linking"></a>
# Linking sites on Kubernetes using YAML

Once sites are linked, services can be exposed and consumed across the application network without the need to open ports or manage inter-site connectivity.

Terminology:

* Connecting site: The site that initiates the link connection.
* Listening site: The site receives the the link connection.

The link direction is not significant, and is typically determined by ease of connectivity. For example, if `east` is behind a firewall and `west` is a cluster on the public cloud, linking from `east` to `west` is the easiest option.

There are two ways of linking sites on Kubernetes using YAML:

* Using `AccessGrant` and `AccessToken` resources to produce a token on the listening site. The link is created when the `AccessToken` is applied to the connecting site. 

* Using a `Link` resource on the listening site. The link is created when the `Link` is applied to the connecting site. 

The advantage of using `AccessGrant` and `AccessToken` resources is that you can limit token usage. By default, a token can only be used once and must be used within 15 minutes to link sites.

The procedures below describe linking an existing site.
Typically, it is easier to configure a site, links and services in a set of files and then create a configured site by placing all the YAML files in a directory, for example `local` and then using the following command to 

<a id="kube-access-yaml"></a>
## Linking sites using  `AccessGrant` and `AccessToken` resources

**Prerequisites**

* Two sites
* The listening site must have `link-access` enabled. For example:
  ```yaml
  apiVersion: skupper.io/v2alpha1
  kind: Site
  metadata:
    name: west
    namespace: west
  spec:
    linkAccess: default
   ```
To link sites, you create `AccessGrant` and `AccessToken` resources on the listening site and apply the  `AccessToken` resource on the connecting site to create the link.


**AccessGrant** is a server-side permission on a listening site that allows redemption of access tokens to create links. It exposes a URL, a secret code, and a CA for issuing certificates. The number of redemptions and the length of the redemption window is configurable.

**AccessToken** is short-lived, usually single-use credential that contains the AccessGrant URL and secret code. A connecting site redeems this token to establish a link to the listening site.

**Procedure**

1. On the listening site, for example `west` namespace, create an `AccessGrant` resource:
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: AccessGrant
   metadata:
     name: grant-west
   spec:
     redemptionsAllowed: 2        # default 1
     expirationWindow: 25m        # default 15m
   ```
   For example, if you created `accessgrant.yaml`:
   ```bash
   kubectl apply -f accessgrant.yaml
   ```
3. Populate environment variables to allow token generation:

   ```bash
   NS="west"
   GRANT="grant-west"
   
   CODE=$(kubectl -n "$NS" get accessgrant "$GRANT" -o jsonpath='{.status.code}')
   CA_RAW=$(kubectl -n "$NS" get accessgrant "$GRANT" -o jsonpath='{.status.ca}')
   # Use bash's %q to escape safely for a single-line YAML string
   CA_ESCAPED=$(printf '%q' "$CA_RAW")

   URL=$(kubectl -n "$NS" get accessgrant "$GRANT" -o jsonpath='{.status.url}')
   ```
   These environment variable settings support the next step of generating the token.

4. Create a token YAML file:
   ```bash
   cat > token.yaml <<EOF
   apiVersion: skupper.io/v2alpha1
   kind: AccessToken
   metadata:
     name: my-token
   spec:
     code: "${CODE}"
     ca: ${CA_ESCAPED}
     url: "${URL}"
   EOF
   ```
   where `token.yaml` is the name of the YAML file that is saved on your local filesystem.


<a id="kube-link-yaml"></a>
## Linking sites using a `link` resource

An alternative approach to linking sites using tokens is to create a `link` resource YAML file using the CLI, and to apply that resource to another site.

**Prerequisites**

* A local kube site
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
   where `<filename>` is the name of a YAML file that is saved on your local filekube.

3. Apply the `link` resource YAML file on a local kube site to create a link:
   ```bash
   mv <filename> ~/.local/share/skupper/namespaces/default/input/resources/
   skupper kube setup --force
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filekube.

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
