---
render_macros: false
---
<!-- Macro rendering is disabled because this page contains literal Go template expressions. -->
<a id="kube-yaml-site-linking"></a>
# Linking sites on Kubernetes using YAML
<!--ASSEMBLY-->

Once sites are linked, services can be exposed and consumed across the application network without the need to open ports or manage inter-site connectivity.

Terminology:

* Connecting site: The site that initiates the link connection.
* Listening site: The site receives the link connection.

The link direction is not significant, and is typically determined by ease of connectivity. For example, if `east` is behind a firewall and `west` is a cluster on the public cloud, linking from `east` to `west` is the easiest option.


<a id="kube-access-yaml"></a>
## Linking sites using `AccessGrant` and `AccessToken` resources
<!--PROCEDURE-->

Use `AccessGrant` and `AccessToken` resources to create a link between two Kubernetes sites using YAML.

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

   ```bash
   URL="$(kubectl get accessgrant grant-west -o template --template '{{ .status.url }}')"
   CODE="$(kubectl get accessgrant grant-west -o template --template '{{ .status.code }}')"
   CA_RAW="$(kubectl get accessgrant grant-west -o template --template '{{ .status.ca }}')"
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

<a id="kube-link-cost-yaml"></a>
## Specifying link cost using YAML
<!--PROCEDURE-->

Link cost is a configurable integer value that influences how Skupper routes
traffic across links between sites.
The routing algorithm favors paths with the lowest total cost from client to
target server.

**📌 NOTE**
For most load-balancing and failover use cases, a [multi-key listener][mkl]
provides more predictable, per-service control than link cost.
Link cost applies to **all services** that traverse a link; it is not
possible to set different costs for distinct services on the same link.

Understanding link cost behavior:

* The default link cost is `1`. Local workloads have an implicit cost of `0`.
* If a connection traverses more than one link, the path cost is the sum of
  all link costs along the path.
* Cost acts as a threshold. When only one path exists, traffic flows on that
  path regardless of cost. If a target becomes unavailable, traffic moves to
  the remaining path regardless of cost.
* When multiple paths exist, traffic flows on the lowest-cost path until the
  number of open connections exceeds the cost of an alternative path. After
  that threshold is reached, new connections are spread across both paths.
* Traffic distribution is statistical, not round robin.

Link cost is set on the `Link` custom resource via `spec.cost`.
The `AccessToken` resource also exposes `spec.linkCost`, which is applied to the `Link` created when the token is redeemed.

**Prerequisites**

* Two or more linked sites.
* The name of the `Link` resource whose cost you want to set.

**Procedure**

**Option A — Set cost when redeeming a token**

Add `linkCost` to the `AccessToken` resource before applying it. When the token is redeemed, the resulting `Link` is created with that cost.

```yaml
apiVersion: skupper.io/v2alpha1
kind: AccessToken
metadata:
  name: my-token
spec:
  url: <grant-url>
  code: <secret-code>
  ca: <ca-cert>
  linkCost: 2
```

Apply it:

```bash
kubectl apply -f token.yaml
```

**Option B — Update cost on an existing link**

1. Find the link name:

   ```bash
   kubectl get links
   ```
   Example output:
   ```
   NAME          STATUS   REMOTE SITE   MESSAGE
   west-6bfn6    Ready    west
   ```

2. Patch the cost on the link:

   ```bash
   kubectl patch link west-6bfn6 --type merge -p '{"spec":{"cost":2}}'
   ```
   
   Or edit the resource directly:
   
   ```bash
   kubectl edit link west-6bfn6
   ```
   
   Set the `cost` field in `spec`:
   
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: Link
   metadata:
     name: west-6bfn6
   spec:
     cost: 2
     endpoints:
       - host: <remote-host>
         name: inter-router
         port: "55671"
       - host: <remote-host>
         name: edge
         port: "45671"
     tlsCredentials: west-6bfn6
   ```

**Verifying link cost**

Check the cost of a specific link:

```bash
kubectl get link west-6bfn6 -o yaml
```

Look for `spec.cost` in the output. Alternatively, for a summary:

```bash
kubectl get links
```

**Additional information**

* The minimum enforced cost is `1`. If `spec.cost` is set to `0` or omitted, the router treats it as `1`.
* For the failover pattern (primary cost `0`/local, backup cost `99999`), set `spec.cost: 99999` on the backup site's `Link` resource.

A common use case for link cost is automatic failover.
You can configure a primary site with an effective cost of `0` (local) and a
backup site with a high link cost, for example `99999`:

- local server — effective cost `0`
- remote backup server — link cost `99999`

In this configuration, all connections are routed to the local server.
If the local server becomes unavailable, traffic fails over to the remote
server regardless of the high cost.

**📌 NOTE**
Skupper does not provide orchestrated failover for stateful applications that
require control over the order in which traffic is redirected.
You must implement that orchestration separately.

For per-service failover or weighted traffic distribution, use a
[multi-key listener][mkl] instead.

[mkl]: ./service-exposure.html#kube-creating-multikeylistener-yaml
<a id="kube-link-custom-certs-yaml"></a>
## Linking sites using `Link` resources and custom certificates

By default, the Skupper V2 controller generates internal Certificate Authorities (CAs) and self-signed certificates.  
For example, it creates certificates to authenticate incoming Skupper links from external Skupper sites.

The CA and server certificate used for this authentication are named `skupper-site-ca` (default signing `Certificate` resource for a Skupper Site) and `skupper-site-server`, respectively.

The server certificate (`skupper-site-server`) issued by the self-signed CA `skupper-site-ca` is issued for the public hostname or IP address associated with the `skupper-router` service. This depends on the ingress method used, for example an OpenShift Route or a Kubernetes LoadBalancer Service.

Although this behavior is automatic, you can override it by providing your own custom server certificate or even your own CA.

**Prerequisites**

* Two sites
* The listening site must have `link-access` enabled
* A server certificate and key for the listening site
* `jq` and `yq` installed if using the kubectl method to generate the `Link` resource

To link sites using custom certificates, you provide a custom server certificate on the listening site and create a `Link` resource on the connecting site that references matching client credentials.

**Procedure**

1. On the listening site, create a secret named `skupper-site-server`, for example:
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: skupper-site-server
   data:
     ca.crt: LS0tLS1C...redacted
     tls.crt: LS0tLS1C...redacted
     tls.key: LS0tLS1C...redacted
   ```
   Apply the secret:
   ```shell
   kubectl delete secret skupper-site-server # delete existing secret
   kubectl apply -f skupper-site-server.yaml
   ```
   
   Make sure the certificate specified in `tls.crt` is valid for the hostname or IP address that will be referenced in your `Link` resource. In this example, consider the server certificate as being valid for the hostname: `skupper.public.host`.

2. Determine the hostname or IP address for the listening site.
   
   In case your Skupper Site is already created, you can find the appropriate Hostname or IP by looking at the Endpoint element of a Site status:
   ```shell
   kubectl get site <site-name> -o json | jq -r '.status.endpoints[0].host'
   ```
   And you will see something like:
   ```
   skupper.public.host
   ```
   
   **_Note:_** Make sure you specify the appropriate namespace when running the commands from this example.
   
   Again, if your Site has already been created, Skupper will recognize your custom secret. You can confirm this with the following command:
   ```shell
   kubectl get certificate.skupper.io skupper-site-server -o json | jq -r '.status.conditions[].message'
   ```
   You should see a message like:
   ```
   Secret exists but is not controlled by skupper
   ```
   This confirms that Skupper has detected your certificate but is not managing it.

3. On the listening site, create client credentials for the connecting site.

   Once your Skupper site is configured to use your custom server certificate, you can create a `Link` resource and an associated client `Secret`. If the `skupper-site-ca` signing `Certificate` resource has been provided, you can create a Certificate resource and Skupper will generate the client Secret to be used, but it is only possible if the signing `Certificate` resource has been provided, otherwise, you have to provide the client Secret yourself.

   If the listening site provides the `skupper-site-ca` issuer, create a `Certificate` resource so that Skupper generates a client secret named `skupper-link`:
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: Certificate
   metadata:
     name: skupper-link
   spec:
     ca: skupper-site-ca
     client: true
     subject: skupper.public.host
   ```
   Apply the resource:
   ```shell
   kubectl apply -f skupper-link-certificate.yaml
   ```
   You should see an output like:
   ```
   certificate.skupper.io/skupper-link created
   ```
   Then a Secret named `skupper-link` should be created and it can be used to compose your link file.
   
   Save the generated secret to a local file for use in the next step:
   ```shell
   kubectl get secret skupper-link -o yaml | yq eval -o=yaml 'del(.metadata.namespace, .metadata.creationTimestamp, .metadata.resourceVersion, .metadata.uid, .metadata.managedFields)' - > client-secret.yaml
   ```

   If you are providing the client certificate yourself, create a secret named `skupper-link`, for example:
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: skupper-link
   data:
     ca.crt: LS0tLS1C...redacted
     tls.crt: LS0tLS1C...redacted
     tls.key: LS0tLS1C...redacted
   ```
   Save this resource locally as `client-secret.yaml` if you want to combine it with a `Link` resource in a single file.

4. On the listening site, create a `Link` resource YAML file.

   Now, regardless of whether Skupper generated your client certificate Secret or if you generated it yourself, to define a Skupper Link, that can be shared with remote sites allowing them to initiate a secure outgoing link to your site, you will need to write a YAML file that contains both documents: a `Link`, and a Client `Secret`.

   You can generate a Link using `kubectl` or manually (as long as retrieve the list of endpoints). Here are these two methods:

   **Option A: Using kubectl with jq and yq**

   The following command uses `kubectl`, `yq`, `jq` and `tee` to extract and compose the information needed to define a Link, storing the Link document into `skupper-link.yaml`:
   ```shell
   endpoints=$(kubectl get site <site-name> -o json | jq -r '.status.endpoints')
   cat << EOF | yq -y --argjson endpoints "${endpoints}" '.spec.endpoints = $endpoints' | tee skupper-link.yaml
   apiVersion: skupper.io/v2alpha1
   kind: Link
   metadata:
     name: skupper-link
   spec:
     cost: 1
     tlsCredentials: skupper-link
   EOF
   ```
   Then you need to combine it in a YAML file that contains both the Link above and the client Secret. Suppose your client Secret is stored in a file named `client-secret.yaml`, you could run:
   ```shell
   echo "---" >> skupper-link.yaml
   cat client-secret.yaml >> skupper-link.yaml
   ```

   **Option B: Manual generation**

   You can retrieve the list of endpoints from the Site definition, using:
   ```shell
   kubectl get site <site-name> -o yaml | yq -y .status.endpoints
   ```
   The command above uses both `kubectl` and `yq`. And the output should be something like:
   ```yaml
   - group: skupper-router
     host: skupper.public.host
     name: inter-router
     port: '55671'
   - group: skupper-router
     host: skupper.public.host
     name: edge
     port: '45671'
   ```

   Then you can create your Link file with:
   ```yaml
   ---
   apiVersion: skupper.io/v2alpha1
   kind: Link
   metadata:
     name: skupper-link
   spec:
     cost: 1
     tlsCredentials: skupper-link
     endpoints:
       - group: skupper-router
         host: skupper.public.host  # The hostname or IP specified in your custom certificate
         name: inter-router
         port: '55671'
       - group: skupper-router
         host: skupper.public.host  # The same hostname or IP
         name: edge
         port: '45671'
   ---
   apiVersion: v1
   kind: Secret
   metadata:
     name: skupper-link
   data:
     ca.crt: LS0tLS1C...redacted        # The trusted CA certificate
     tls.crt: LS0tLS1C...redacted       # The client certificate
     tls.key: LS0tLS1C...redacted       # The corresponding private key
   ```

5. Securely transfer the `Link` resource YAML file to the context of the connecting site.
   If you have both sites available from your terminal session, this step is not required.

   **📌 NOTE**
   Access to this file provides access to the application network.
   Protect it appropriately.

6. On the connecting site, apply the YAML file and check status:
   ```shell
   kubectl apply -f skupper-link.yaml
   kubectl get link
   NAME            STATUS   REMOTE SITE   MESSAGE
   skupper-link    Ready    my-site       OK
   ```
