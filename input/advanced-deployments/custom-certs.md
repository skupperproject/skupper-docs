## Custom Certificates

By default, the Skupper V2 controller generates internal Certificate Authorities (CAs) and self-signed certificates.  
For example, it creates certificates to authenticate incoming Skupper links from external Skupper sites.

The CA and server certificate used for this authentication are named `skupper-site-ca` (default issuer for a Skupper Site) and `skupper-site-server`, respectively.

The self-signed server certificate (`skupper-site-server`) is issued for the public hostname or IP address associated with the `skupper-router` service. This depends on the ingress method used, for example an OpenShift Route or a Kubernetes LoadBalancer Service.

Although this behavior is automatic, you can override it by providing your own custom server certificate or even your own CA.

### Providing a Custom Server Certificate

To authenticate incoming Skupper links using your own server certificate, create a Kubernetes Secret named `skupper-site-server` in the namespace where your Skupper site is (or will be) deployed:

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

Make sure the certificate specified in `tls.crt` is valid for the hostname or IP address that will be referenced in your `Link` resource. In this example, consider the server certificate as being valid for the hostname: `skupper.public.host`.

In case your Skupper Site is already created, you can find the appropriate Hostname or IP by looking at the Endpoint element of a Site status, like in the example below:

```bash
kubectl get site -o json | jq -r .items[].status.endpoints[0].host
```

And you will see something like:

```
skupper.public.host
```

**_Note:_** Make sure you specify the appropriate namespace when running the commands from this example.

Again, if your Site has already been created, Skupper will recognize your custom secret. You can confirm this with the following command:

```bash
kubectl get certificate skupper-site-server -o json | jq -r .status.conditions[].message
```

You should see a message like:

```
Secret exists but is not controlled by skupper
```

This confirms that Skupper has detected your certificate but is not managing it.

### Generating a Link for Remote Sites

Once your Skupper site is configured to use your custom server certificate, you can create a `Link` resource and an associated client `Secret`. If the `skupper-site-ca` Issuer has been provided, you can create a Certificate resource and Skupper will generate the client Secret to be used, but it is only possible if the Issuer has been provided, otherwise, you have to provide the client Secret yourself.

Here is how you can generate a Secret for a client certificate _(again, only if the Issuer has been provided)_:

```bash
cat << EOF | kubectl create -f -
apiVersion: skupper.io/v2alpha1
kind: Certificate
metadata:
  name: skupper-link
spec:
  ca: skupper-site-ca
  client: true
  subject: skupper.public.host
EOF
```

You should see an output like:

```
certificate.skupper.io/skupper-link created
```

Then a Secret named `skupper-link` should be created and it can be used to compose your link file.

Now, regardless of whether Skupper generated your client certificate Secret or if you generated it yourself, to define a Skupper Link, that can be shared with remote sites allowing them to initiate a secure outgoing link to your site, you will need to write a YAML file that contains both documents:

- A `Link`, and
- A Client `Secret`

You can generate a Link using the `skupper` CLI, using `kubectl` or manually (as long as retrieve the list of endpoints).
Here are these three examples:

#### Using the skupper CLI

This is the easiest way to generate a Link.

There are three ways you can run it.

1. If you provided the `skupper-site-ca` Issuer to Skupper:

```bash
skupper link generate
```

2. If your client certificates is defined as a Kubernetes secret named skupper-link:

```bash
skupper link generate --tls-credentials skupper-link
```

3. If you are providing the `skupper-link` client certificate yourself:

```bash
skupper link generate --generate-credential=false --tls-credentials=skupper-link
```

In this last example, you will need to combine the Link resource returned by the command
above with the client Secret named `skupper-link`. Suppose your client Secret is stored locally
on a file named `client-secret.yaml`, you could run:

```bash
skupper link generate --generate-credential=false --tls-credentials=skupper-link; echo "---"; cat client-secret.yaml
```

#### Using kubectl

The following command uses `kubectl`, `yq`, `jq` and `tee` to extract and compose the information needed to define a Link, storing the Link document into `skupper-link.yaml`.

```bash
endpoints=$(kubectl get site -o json | jq -r '.items[].status.endpoints')
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

Then you need to combine it in a YAML file that contains both the Link above and the client Secret.
Suppose your client Secret is stored in a file named `client-secret.yaml`, you could run:

```bash
echo "---" >> skupper-link.yaml
cat client-secret.yaml >> skupper-link.yaml
```

#### Manually generation

You can retrieve the list of endpoints from the Site definition, using:

```bash
kubectl get site -o yaml | yq -y .items[].status.endpoints
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