---
body_class: object concept
refdog_links:
- title: Service exposure
  url: /docs/refdog/topics/service-exposure.html
- title: Listener concept
  url: /docs/refdog/concepts/listener.html
- title: Connector concept
  url: /docs/refdog/concepts/connector.html
render_macros: false
---

# Routing key concept

A routing key is a string identifier for matching
[listeners](listener.html) and [connectors](connector.html).

<figure>
  <img src="images/routing-key-model.svg"/>
  <figcaption>The routing key model</figcaption>
</figure>

A routing key has zero or more listeners and zero or more
connectors.  A service is exposed on the application network when it
has at least one listener and one connector, matched by routing key.

<figure>
  <img src="images/routing-key-1.svg"/>
  <figcaption>A workload exposed as a service in a remote
  site</figcaption>
</figure>

<figure>
  <img src="images/routing-key-2.svg"/>
  <figcaption>A routing key with two listeners and two
  connectors</figcaption>
</figure>
