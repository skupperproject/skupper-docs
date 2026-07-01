---
render_macros: false
---
<!-- Macro rendering is disabled because this page contains literal Go template expressions. -->
<a id="kube-yaml-custom-certs"></a>
# Linking sites using custom certificates
<!--ASSEMBLY-->

By default, the Skupper controller generates internal Certificate Authorities (CAs) and self-signed certificates.  
For example, it creates certificates to authenticate incoming Skupper links from external Skupper sites.

The CA and server certificate used for this authentication are named `skupper-site-ca` (default signing `Certificate` resource for a Skupper Site) and `skupper-site-server`, respectively.

Although this behavior is automatic, you can override it by providing your own custom server certificate or even your own CA.

This document describes two approaches for using custom certificates:

* **Using a custom `RouterAccess` and custom certificates** - Manually define the `RouterAccess` CR with your own certificate (`linkAccess` is not enabled)

* **Using `Link` resources and custom certificates** - Override the default `skupper-site-server` certificate before `linkAccess` is enabled


**Key differences between approaches**

| | `linkAccess` | `RouterAccess` |
|---|---|---|
| Who creates `RouterAccess` | Skupper controller (auto) | You (manually) |
| `generateTlsCredentials` | `true` | `false` |
| Secret name | Must be `skupper-site-server` | Any name you choose |
| Site delete/recreate needed | Yes, to prevent overwrite | No |
| Skupper overwrites your cert | Yes, unless pre-created | Never |


<a id="kube-router-access-custom-certs-yaml"></a>
## Linking sites using a custom `RouterAccess`, and custom certificates
<!--PROCEDURE-->

By default, when you set `spec.linkAccess` on a `Site`, the Skupper controller automatically creates a `RouterAccess` named `skupper-router` with `generateTlsCredentials: true` and `tlsCredentials: skupper-site-server`.

The alternative is to define the `RouterAccess` CR yourself with `generateTlsCredentials: false` and point `tlsCredentials` at a Secret you supply. When `generateTlsCredentials` is false, the Skupper controller recognizes your custom certificate and will not modify it.

**Prerequisites**

* Two sites
* A server certificate and key for the listening site
* `jq` and `yq` (mikefarah/yq, the Go-based implementation) installed if using the kubectl method to generate the `Link` resource

**Procedure**

1. On the listening site, create a `Site` CR **without** `spec.linkAccess` (or with `spec.linkAccess: none`):
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: Site
   metadata:
     name: my-site
   spec: {}
   ```
   Apply it:
   ```shell
   kubectl apply -f site.yaml
   ```
   Because `spec.linkAccess` is not set, the controller will not auto-create any `RouterAccess`.

2. On the listening site, create a Secret containing your custom server certificate. You can name it anything — this example uses `my-server-cert`:
   ```yaml
   apiVersion: v1
   kind: Secret
   type: "kubernetes.io/tls"
   metadata:
     name: my-server-cert
   data:
     ca.crt: LS0tLS1C...redacted
     tls.crt: LS0tLS1C...redacted
     tls.key: LS0tLS1C...redacted
   ```
   Apply it:
   ```shell
   kubectl apply -f my-server-cert.yaml
   ```
   Make sure the certificate in `tls.crt` is valid for the hostname or IP address that will be referenced in your `Link` resource. In this example, consider it valid for `skupper.public.host`.

3. On the listening site, create a `RouterAccess` CR that references your Secret and sets `generateTlsCredentials: false`:
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: RouterAccess
   metadata:
     name: my-router-access
   spec:
     generateTlsCredentials: false
     tlsCredentials: my-server-cert
     accessType: loadbalancer   # or "route", "ingress", etc.
     roles:
       - name: inter-router
         port: 55671
       - name: edge
         port: 45671
   ```
   Apply it:
   ```shell
   kubectl apply -f my-router-access.yaml
   ```
   Because `generateTlsCredentials: false`, Skupper will use your Secret as-is and will never overwrite it.

4. Determine the hostname or IP address for the listening site.

   Check the `RouterAccess` status for the resolved endpoints:
   ```shell
   kubectl get routeraccess my-router-access -o json | jq -r '.status.endpoints[0].host'
   ```
   You should see something like:
   ```
   skupper.public.host
   ```

5. On the listening site, create client credentials for the connecting site.

   Since Skupper still creates the `skupper-site-ca` signing `Certificate` resource, you can use it to generate a client secret automatically. Create a `Certificate` resource:
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: Certificate
   metadata:
     name: skupper-link
   spec:
     ca: skupper-site-ca
     client: true
     subject: skupper-client
   ```
   Apply it:
   ```shell
   kubectl apply -f skupper-link-certificate.yaml
   ```
   Save the generated Secret for use in the next step:
   ```shell
   kubectl get secret skupper-link -o yaml | yq eval -o=yaml 'del(.metadata.namespace, .metadata.creationTimestamp, .metadata.resourceVersion, .metadata.uid, .metadata.managedFields)' - > client-secret.yaml
   ```

   If you are providing the client certificate yourself, create a Secret named `skupper-link` directly and save it as `client-secret.yaml`.

6. On the listening site, create a `Link` resource YAML file.

   **Option A: Using kubectl with jq and yq**
   ```shell
   kubectl get routeraccess my-router-access -o json | jq '{
     apiVersion: "skupper.io/v2alpha1",
     kind: "Link",
     metadata: {name: "skupper-link"},
     spec: {
       cost: 1,
       tlsCredentials: "skupper-link",
       endpoints: .status.endpoints
     }
   }' | yq -P > skupper-link.yaml
   echo "---" >> skupper-link.yaml
   cat client-secret.yaml >> skupper-link.yaml
   ```

   **Option B: Manual generation**

   Retrieve the endpoints:
   ```shell
   kubectl get routeraccess my-router-access -o yaml | yq '.status.endpoints'
   ```
   Then compose the file manually:
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
         host: skupper.public.host
         name: inter-router
         port: '55671'
       - group: skupper-router
         host: skupper.public.host
         name: edge
         port: '45671'
   ---
   apiVersion: v1
   kind: Secret
   type: "kubernetes.io/tls"
   metadata:
     name: skupper-link
   data:
     ca.crt: LS0tLS1C...redacted
     tls.crt: LS0tLS1C...redacted
     tls.key: LS0tLS1C...redacted
   ```

7. Securely transfer the `Link` resource YAML file to the connecting site.

   **📌 NOTE**
   Access to this file provides access to the application network.
   Protect it appropriately.

8. On the connecting site, apply the YAML file and check status:
   ```shell
   kubectl apply -f skupper-link.yaml
   kubectl get link
   NAME            STATUS   REMOTE SITE   MESSAGE
   skupper-link    Ready    my-site       OK
   ```

<a id="kube-link-custom-certs-yaml"></a>
## Linking sites using `Link` resources and custom certificates
<!--PROCEDURE-->

The server certificate (`skupper-site-server`) issued by the self-signed CA `skupper-site-ca` is issued for the public hostname or IP address associated with the `skupper-router` service. This depends on the ingress method used, for example an OpenShift Route or a Kubernetes LoadBalancer Service.

You can override this behavior by providing your own custom server certificate.

**Prerequisites**

* Two sites
* The listening site must have `link-access` enabled
* A server certificate and key for the listening site
* `jq` and `yq` (mikefarah/yq, the Go-based implementation) installed if using the kubectl method to generate the `Link` resource

To link sites using custom certificates, you provide a custom server certificate on the listening site and create a `Link` resource on the connecting site that references matching client credentials.

NOTE: In this procedure you delete and recreate your site to make sure the certificate configuration is applied.

**Procedure**

1. On the listening site, create a secret named `skupper-site-server`, for example:
   ```yaml
   apiVersion: v1
   kind: Secret
   type: "kubernetes.io/tls"
   metadata:
     name: skupper-site-server
   data:
     ca.crt: LS0tLS1C...redacted
     tls.crt: LS0tLS1C...redacted
     tls.key: LS0tLS1C...redacted
   ```
   Apply the secret while deleting and recreating the site:
   ```shell
   kubectl delete site <site-name> # delete the site
   kubectl apply -f skupper-site-server.yaml
   kubectl apply -f site.yaml # recreate the site
   ```
   NOTE: If you attempt to apply the secret on an existing site, the Skupper controller overwrites your changes. Make sure to create the secret before creating your site.

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

   Once your Skupper site is configured to use your custom server certificate, you can create a `Link` resource and an associated client `Secret`. Since Skupper always creates the `skupper-site-ca` signing `Certificate` resource on Kubernetes sites, you can use it to generate client credentials automatically. If you have replaced `skupper-site-ca` with a custom CA that Skupper cannot use for signing, you will need to provide the client `Secret` yourself.

   To use the automatically created `skupper-site-ca` issuer, create a `Certificate` resource so that Skupper generates a client secret named `skupper-link`:
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
   type: "kubernetes.io/tls"
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

   The following command uses `kubectl`, `jq`, and `yq` to extract and compose the information needed to define a Link, storing the Link document into `skupper-link.yaml`:
   ```shell
   kubectl get site <site-name> -o json | jq '{
     apiVersion: "skupper.io/v2alpha1",
     kind: "Link",
     metadata: {name: "skupper-link"},
     spec: {
       cost: 1,
       tlsCredentials: "skupper-link",
       endpoints: .status.endpoints
     }
   }' | yq -P > skupper-link.yaml
   ```
   Then you need to combine it in a YAML file that contains both the Link above and the client Secret. Suppose your client Secret is stored in a file named `client-secret.yaml`, you could run:
   ```shell
   echo "---" >> skupper-link.yaml
   cat client-secret.yaml >> skupper-link.yaml
   ```

   **Option B: Manual generation**

   You can retrieve the list of endpoints from the Site definition, using:
   ```shell
   kubectl get site <site-name> -o yaml | yq '.status.endpoints'
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
   type: "kubernetes.io/tls"
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
