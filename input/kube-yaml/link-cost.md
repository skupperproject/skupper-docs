<a id="kube-link-cost-yaml"></a>
# Specifying link cost using YAML
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
