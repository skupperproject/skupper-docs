<a id="kube-link-cost-cli"></a>
# Specifying link cost
<!--PROCEDURE-->

Link cost is a configurable integer value that influences how Skupper routes
traffic across links between sites.
The routing algorithm favors paths with the lowest total cost from client to
target server.

**📌 NOTE**
For most load-balancing and failover use cases, a [multi-key listener][mkl]
provides per-service control.
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

The following procedure describes how to set link cost in various scenarios:

**Procedure**

1. To redeem a token and specify the cost:

   ```bash
   skupper token redeem <filename> --link-cost <integer-cost>
   ```
   where `<integer-cost>` is an integer greater than `1` and traffic favors
   lower-cost links.

   For example, to redeem a token and set the link cost to `2`:
   ```
   skupper token redeem token.yaml --link-cost 2
   ```


2. To Update the cost on an existing link:

   ```
   skupper link update <link-name> --cost <integer-cost>
   ```
   For example:
   ```
   skupper link update west-6bfn6 --cost 2
   Waiting for status...
   Link "west-6bfn6" is ready.
   ```

3. To check the cost of a specific link:

   ```
   skupper link status <link-name>
   ```
   Example output:
   ```
   Name:     west-6bfn6
   Status:   Ready
   Message:  <none>
   Cost:     2
   ```

**Additional information**

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

[mkl]: ../kube-yaml/service-exposure.html#kube-creating-multikeylistener-yaml
