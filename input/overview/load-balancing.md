<a id="overview-load-balancing"></a>
# Skupper load balancing and failover
<!--CONCEPT-->

Skupper balances active connections across sites and reroutes traffic when a site fails.

Skupper enables load balancing and failover across servers located across the application network.
Specifically, Skupper balances **active TCP connections** across workloads deployed in distinct sites.
If a workload at one site becomes unavailable, traffic is automatically rerouted to available sites. 
For example, if you deploy the same backend code on two sites and expose the backend on the application network, concurrent requests from a third site to the backend service are processed by both sites.

## Preferred approach: Multi-key listeners

A [multi-key listener][mkl] provides per-service control over load balancing and failover by binding a single endpoint to multiple routing keys (connectors).
This is the **recommended** approach for most use cases because it offers:

* **Per-service configuration** — Each service can have its own distribution strategy, independent of network topology.
* **Predictable behavior** — Traffic distribution is explicitly controlled by strategy, not influenced by connection timing or link metrics.
* **Two strategies**:
  * **weighted** — Proportional distribution across routing keys. For example, assign weights of `25` and `75` to send a quarter of TCP connections to the first backend and three-quarters to the second.
  * **priority** — Failover with preference order. Traffic uses the first available routing key; if that connector becomes unavailable, traffic automatically shifts to the next routing key in the list.

For configuration details and examples, see [Creating a multi-key listener using YAML][mkl].

## Alternative: Link cost

Link cost is a configurable integer value that influences how Skupper routes traffic across **all services** that traverse a link between two sites.
The routing algorithm favors paths with the lowest total cost from client to target server.

**📌 NOTE**
Link cost applies to **all services** on a link and cannot be set differently for individual services.
For per-service control, use a [multi-key listener][mkl] instead.

**Understanding link cost behavior**

* The default link cost is `1`. Local workloads have an implicit cost of `0`.
* If a connection traverses more than one link, the path cost is the sum of all link costs along the path.
* Cost acts as a threshold. When only one path exists, traffic flows on that path regardless of cost. If a target becomes unavailable, traffic moves to the remaining path regardless of cost.
* When multiple paths exist, traffic flows on the lowest-cost path until the number of open connections exceeds the cost of an alternative path. After that threshold is reached, new connections are spread across both paths.
* Traffic distribution is statistical, not round robin.

**Using link cost for failover**

You can configure link cost so that a primary location handles all traffic until failure, then traffic fails over to a backup location.
To achieve this, set the cost from the client to the backup server very high, for example `99999`:

- local server — effective cost `0`
- remote backup server — link cost `99999`

In this configuration, all connections are routed to the local server.
If the local server becomes unavailable, traffic fails over to the remote server regardless of the high cost.

**📌 NOTE**
Skupper does not provide orchestrated failover for stateful applications that require control over the order in which traffic is redirected.
You must implement that orchestration separately.

For details on configuring link cost, see:
* [Specifying link cost using the CLI][link-cost-cli]
* [Specifying link cost using YAML][link-cost-yaml]

[link-cost-cli]: ../kube-cli/link-cost.html
[link-cost-yaml]: ../kube-yaml/link-cost.html
[mkl]: ../kube-yaml/service-exposure.html#kube-creating-multikeylistener-yaml
