---
render_macros: false
---

# Attached connectors

- An attached connector is one not directly in the site namespace but
  in a peer namespace.
- Useful for sharing services across networks.
- Requires the router namespace and the workload namespace to opt in
  to the attachment.
- The router side controls the routing key.  The workload side
  controls the selector.
- siteNamespace and connectorNamespace must correspond.
- AttachedConnector and AttachedConnectorBinding must have matching
  names.
- The connector side is responsible for selecting pods, while the
  binding side controls the routing key.
- If you want to expose a workload (say a database) in multiple
  networks, you need multiple AttachedConnectors, one for each
  corresponding binding that resides in a particular site belonging to
  a network.
- You can't create attached connectors with the CLI.  You have to use
  YAML resources.


An _attached connector_ is a connector in a peer namespace.

<figure>
  <img src="../concepts/images/attached-connector-1.svg"/>
  <figcaption>XXX</figcaption>
</figure>
