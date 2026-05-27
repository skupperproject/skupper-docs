---
body_class: object concept
refdog_links:
- title: Service exposure
  url: /docs/refdog/topics/service-exposure.html
- title: MultiKeyListener resource
  url: /docs/refdog/resources/multi-key-listener.html
- title: Listener concept
  url: /docs/refdog/concepts/listener.html
- title: Connector concept
  url: /docs/refdog/concepts/connector.html
- title: Routing key concept
  url: /docs/refdog/concepts/routing-key.html
render_macros: false
---

# Multi-key-listener concept

A multi-key listener binds a single local connection endpoint to
multiple [connectors](connector.html) in remote [sites](site.html)
using a strategy that matches multiple [routing keys](routing-key.html).

Unlike a standard [listener](listener.html) which uses a single
routing key to match with connectors, a multi-key listener can route
to multiple connectors using either priority-based failover or
weighted load balancing.

<figure>
  <img src="images/multi-key-listener-1.svg"/>
  <figcaption>Weighted strategy distributes traffic proportionally across multiple routing keys</figcaption>
</figure>

A multi-key listener exposes a single host and port endpoint that
distributes traffic to different connectors based on its configured
strategy.  This allows you to aggregate multiple backend services
behind a single service endpoint.

**Key idea:** The multi-key listener does not choose a remote IP
address. It chooses **routing keys**. Connectors that advertise
those routing keys forward the streams to their local workloads.

## Multi-key listeners vs link cost

Multi-key listeners provide predictable, client-side traffic control
that is **not influenced by link costs**. This is an important
distinction from standard listeners.

When multiple [connectors](connector.html) share the same routing
key, the router distributes TCP connections across matching
connectors based on associated link costs. However, this
configuration can be unpredictable in real-world situations for use
cases other than failover.

With standard listeners, you can configure failover behavior by
setting the link cost from the client to the backup server very high
(for example, 9999). This ensures a specific location handles all
traffic until failure, then fails over to a different location.

Multi-key listeners with the **priority strategy** provide an
alternative, more explicit approach to failover that does not depend
on link costs. Similarly, the **weighted strategy** provides
predictable load balancing without the unpredictability of link cost
calculations.

**Note:** If multiple multi-key listeners reference the same set of
routing keys, each listener calculates weights and assigns
connections autonomously. There is no coordination or shared state
between listeners when making load-balancing decisions.

## Strategies

Multi-key listeners support two routing strategies:

### Priority strategy

The priority strategy routes 100% of traffic to the first routing key
in the list that has a reachable connector. If that connector becomes
unavailable, traffic automatically fails over to the next routing key
in the list.

Use the priority strategy when you want:
- **High availability** with automatic failover
- **Active-standby** configurations where one backend is preferred
- **Regional preference** where one site is preferred over others

### Weighted strategy

The weighted strategy distributes traffic across multiple routing keys
in proportion to their assigned weights. Routing keys with higher
weights receive a larger share of the traffic.

Use the weighted strategy when you want:
- **Load balancing** across multiple backends
- **Traffic distribution** based on capacity (e.g., 70% to one site, 30% to another)
- **Equal distribution** when all weights are the same

## Use cases

**High availability**: Use a priority strategy to route to a primary
database in one site, automatically failing over to a standby database
in another site if the primary becomes unavailable.

**Load balancing**: Use a weighted strategy to distribute API requests
across backends in multiple geographic regions, with weights based on
capacity or proximity.

**Geographic distribution**: Use a weighted strategy to balance traffic
across multiple data centers, adjusting weights based on load or
performance characteristics.
