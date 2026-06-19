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

**Key idea:** The multi-key listener is not limited to a single routing key.
It chooses from a set of routing keys. Connectors that advertise
those routing keys forward the streams to their local workloads.

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
weights receive a larger share of incoming TCP connections.

Use the weighted strategy when you want:
- **Load balancing** across multiple backends
- **Traffic distribution** based on capacity (e.g., 70% to one site, 30% to another)
- **Equal distribution** when all weights are the same

**Note:** The weighted strategy does not guarantee an exact distribution of traffic, 
especially in small samples, but over time it will approximate the configured weights, 
using a probabilistic approach to routing decisions.

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


**Note:** If multiple multi-key listeners reference the same set of
routing keys, each listener calculates weights and assigns
connections autonomously. There is no coordination or shared state
between listeners when making load-balancing decisions.


## Multi-key listeners and link cost

Multi-key listeners and link cost are independent mechanisms that
work together to control traffic routing.

**Multi-key listeners** select between routing keys using the
configured strategy (priority or weighted). This selection happens
at the listener and is independent of link costs.

**Link cost** determines which connector to use when multiple
connectors share the same routing key. This applies to both standard
listeners and multi-key listeners.

For example, with a weighted multi-key listener:
1. The listener's strategy selects a routing key (e.g., `east-backend`)
2. If multiple connectors use that routing key, link cost determines which connector handles the connection
3. The next connection may select a different routing key based on the weights

Multi-key listeners with the **priority strategy** provide explicit
failover control at the routing key level, independent of link costs.
The **weighted strategy** provides predictable load balancing across
routing keys, while link cost still affects connector selection
within each routing key.

