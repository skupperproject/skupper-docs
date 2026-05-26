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
  <img src="images/routing-key-model.svg"/>
  <figcaption>Multi-key listeners match multiple routing keys</figcaption>
</figure>

A multi-key listener exposes a single host and port endpoint, but
routes traffic to different connectors based on its configured
strategy.  This allows you to aggregate multiple backend services
behind a single service endpoint.

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

## Platform implementation

On Kubernetes, a multi-key listener is implemented as a
[Service][kube-service] with custom routing logic in the Skupper
router.  On Docker, Podman, and Linux, it is a listening socket bound
to a local network interface.

[kube-service]: https://kubernetes.io/docs/concepts/services-networking/service/

The Skupper router monitors the availability of connectors for each
routing key and adjusts traffic routing based on the configured
strategy.
