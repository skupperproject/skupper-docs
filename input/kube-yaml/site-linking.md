<a id="kube-yaml-site-linking"></a>
# Linking sites on Kubernetes using YAML

Once sites are linked, services can be exposed and consumed across the application network without the need to open ports or manage inter-site connectivity.

Terminology:

* Connecting site: The site that initiates the link connection.
* Listening site: The site receives the link connection.

The link direction is not significant, and is typically determined by ease of connectivity. For example, if `east` is behind a firewall and `west` is a cluster on the public cloud, linking from `east` to `west` is the easiest option.


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

**AccessGrant** is a permission on a listening site that allows redemption of access tokens to create links. 
The component it gives permission to is the **GrantServer** which is a HTTPS server that ultimately sets up the link.

The GrantServer provides a URL, a secret code, and a cert that are bundled together to form an AccessToken.
The number of times an AccessToken can be redeemed and how long it remains active are both configurable. 
On OpenShift, the GrantServer is exposed by a Route, while other systems use a LoadBalancer to make it accessible.

**AccessToken** is short-lived, usually single-use credential that contains the AccessGrant URL, secret code and a cert to establish a secure connection to the GrantServer. 
A connecting site redeems this token for a `Link` resource to establish a link to the listening site.

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
   For example, if you created `accessgrant.yaml`, apply and check status:
   ```shell
   kubectl apply -f accessgrant.yaml
   
   kubectl get accessgrants
   
   NAME         REDEMPTIONS ALLOWED   REDEMPTIONS MADE   EXPIRATION             STATUS   MESSAGE
   grant-west   20                    20                 2025-10-15T12:33:04Z   Ready    OK
   ```

2. On the listening site, populate environment variables to allow token generation:

   ```shell
   URL="$(kubectl get accessgrant grant-west -o template --template '{{{ .status.url }}}')"
   CODE="$(kubectl get accessgrant grant-west -o template --template '{{{ .status.code }}}')"
   CA_RAW="$(kubectl get accessgrant grant-west -o template --template '{{{ .status.ca }}}')"
   ```
   
   These environment variable settings support the next step of generating the token.

   * URL is the URL of the GrantServer
   * CODE is the secret code to access the GrantServer
   * CA_RAW is the cert required to establish a HTTPS connection to the GrantServer

3. On the listening site, create a token YAML file:
   ```shell
   cat > token.yaml <<EOF
   apiVersion: skupper.io/v2alpha1
   kind: AccessToken
   metadata:
     name: token-to-west
   spec:
     code: "$(printf '%s' "$CODE")"
     ca: |- 
   $(printf '%s\n' "$CA_RAW" | sed 's/^/    /')
     url: "$(printf '%s' "$URL")"
   EOF
   ```
   where `token.yaml` is the name of the YAML file that is saved on your local filesystem.

   **📌 NOTE**
   Access to this file provides access to the application network. 
   Protect it appropriately.

4. Securely transfer the `token.yaml` file to context of the connecting site.
   If you have both sites available from your terminal session, this step is not required.

5. On the connecting site, apply the token and check status:
   ```shell
   kubectl apply -f token.yaml
   kubectl get accesstokens 
   NAME            URL                                                                REDEEMED   STATUS   MESSAGE
   token-to-west   https://10.110.160.132:9090/87426fa9-5623-49af-a612-47d33b7a4200   true       Ready    OK
   ```
   The GrantServer has validated the AccessToken and redeemed it for a `Link` resource.
   The connecting site uses `Link` resource to establish an mTLS connection between routers.

6. On the connecting site, check link status:
   ```shell
   kubectl get link
   NAME            STATUS   REMOTE SITE   MESSAGE
   token-to-west   Ready    my-site       OK
   ```