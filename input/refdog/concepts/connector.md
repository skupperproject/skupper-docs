---
body_class: object concept
refdog_links:
- title: Service exposure
  url: /docs/refdog/topics/service-exposure.html
- title: Connector resource
  url: /docs/refdog/resources/connector.html
- title: Connector command
  url: /docs/refdog/commands/connector/index.html
- title: Listener concept
  url: /docs/refdog/concepts/listener.html
- title: Routing key concept
  url: /docs/refdog/concepts/routing-key.html
render_macros: false
---

# Connector concept

A connector binds a local [workload](workload.html) to
[listeners](listener.html) in remote [sites](site.html).  Listeners
and connectors are matched using [routing keys](routing-key.html).

<figure>
  <img src="images/connector-model.svg"/>
  <figcaption>The connector model</figcaption>
</figure>

<figure>
  <img src="images/routing-key-model.svg"/>
  <figcaption>The routing key model</figcaption>
</figure>

A site has zero or more connectors.  Each connector has an
associated workload and routing key.  The workload can be specified
as a Kubernetes pod selector or as the host and port of a local
network service.  The routing key is a string identifier that binds
the connector to listeners in remote sites.

On Kubernetes, the workload is usually specified using a pod
[selector][kube-selector].  On Docker, Podman, and Linux, it is
specified using a host and port.

[kube-selector]: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

<figure>
  <img src="images/service-1.svg"/>
  <figcaption>Client connections forwarded to servers</figcaption>
</figure>

Skupper routers forward client connections across the network from
listeners to connectors with matching routing keys.  The connectors
then forward the client connections to the workload servers.

<figure>
  <img src="images/connector-1.svg"/>
  <figcaption>A database service with connectors in two
  sites</figcaption>
</figure>
