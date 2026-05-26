---
body_class: object resource
refdog_links:
- title: Service exposure
  url: /docs/refdog/topics/service-exposure.html
- title: Multi-key-listener concept
  url: /docs/refdog/concepts/multi-key-listener.html
- title: Multi-key-listener concept
  url: /docs/refdog/concepts/multi-key-listener.html
- title: Routing key concept
  url: /docs/refdog/concepts/routing-key.html
- title: Connector resource
  url: /docs/refdog/resources/connector.html
- title: Listener resource
  url: /docs/refdog/resources/listener.html
refdog_object_has_attributes: true
render_macros: false
---

# MultiKeyListener resource

A multi-key listener binds a single local host and port to multiple
routing keys in remote [sites](site.html). Use a multi-key listener
when you want one service endpoint to aggregate traffic from multiple
[connectors](connector.html).

Unlike a standard [listener](listener.html) which maps to a single
routing key, a MultiKeyListener can route to multiple connectors using
either priority-based or weighted distribution strategies.

## Examples

A weighted multi-key listener that distributes traffic evenly across
multiple backends:

~~~ yaml
apiVersion: skupper.io/v2alpha1
kind: MultiKeyListener
metadata:
  name: mkl-backend
spec:
  host: mkl-backend
  port: 9092
  strategy:
    weighted:
      routingKeys:
        east-backend: 1
        west-backend: 1
~~~

A priority-based multi-key listener that prefers one routing key and
falls back to another if unavailable:

~~~ yaml
apiVersion: skupper.io/v2alpha1
kind: MultiKeyListener
metadata:
  name: mkl-backend-priority
spec:
  host: mkl-backend-priority
  port: 9095
  strategy:
    priority:
      routingKeys:
        - east-backend-http
        - west-backend-http
~~~

## Metadata properties

<div class="attribute">
<div class="attribute-heading">
<h3 id="metadata-name">name</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The name of the resource.

<table class="fields"><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/overview/working-with-objects/names/">Kubernetes object names</a></td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="metadata-namespace">namespace</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The namespace of the resource.

<table class="fields"><tr><th>See also</th><td><a href="/docs/refdog/concepts/platform.html">Platform concept</a>, <a href="https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/">Kubernetes namespaces</a></td></table>

</div>
</div>

## Spec properties

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-host">host</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The hostname or IP address of the local listener. Clients
at this site use the listener host and port to
establish connections to the remote service.

<table class="fields"><tr><th>Updatable</th><td>True</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-port">port</h3>
<div class="attribute-type-info">integer</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The port of the local listener. Clients at this site use
the listener host and port to establish connections to
the remote service.

<table class="fields"><tr><th>Updatable</th><td>True</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-strategy">strategy</h3>
<div class="attribute-type-info">object</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

Strategy for routing traffic from the local listener endpoint to one or
more connector instances by routing key.

Must specify exactly one of:
- `priority`: Route to routing keys in priority order (failover)
- `weighted`: Distribute traffic across routing keys by weight (load balancing)

**Note:** The strategy is immutable and cannot be changed after creation.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-strategy.priority">strategy.priority</h3>
<div class="attribute-type-info">None</div>
</div>
<div class="attribute-body">

Priority-based routing strategy. Uses the first routing key in the
list that is available for traffic. If the connector becomes
unavailable, the listener matches with the next available routing
key in the list.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-strategy.priority.routing-keys">strategy.priority.routingKeys</h3>
<div class="attribute-type-info">array</div>
</div>
<div class="attribute-body">

Ordered list of routing keys to route traffic to, from highest to
lowest priority. Must contain 1-256 unique routing keys.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-strategy.weighted">strategy.weighted</h3>
<div class="attribute-type-info">None</div>
</div>
<div class="attribute-body">

Weighted routing strategy. Uses the routing keys in proportion to
the assigned weights. Routing keys with higher weights receive a
larger portion of the traffic. If all keys are assigned the same
weight, traffic is split equally between them.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-strategy.weighted.routing-keys">strategy.weighted.routingKeys</h3>
<div class="attribute-type-info">object</div>
</div>
<div class="attribute-body">

Mapping of routing keys to their weight values. Must contain 1-256
routing keys. For example, if `backend1` is assigned 25 and
`backend2` is assigned 75, then only a quarter of the TCP
connections are directed to `backend1`.



</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-tls-credentials">tlsCredentials</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

The name of a bundle of TLS certificates used for secure
client-to-router communication. The bundle contains the
server certificate and key. It optionally includes the
trusted client certificate (usually a CA) for mutual TLS.

On Kubernetes, the value is the name of a Secret in the
current namespace. On Docker, Podman, and Linux, the value is
the name of a directory under `input/certs/` in the current
namespace.

<table class="fields"><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets">Kubernetes TLS secrets</a></td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-require-client-cert">requireClientCert</h3>
<div class="attribute-type-info">boolean</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

Indicates that clients must present valid certificates to the
listener to connect. Requires `tlsCredentials` to be configured
with a trusted CA certificate.

<table class="fields"><tr><th>Default</th><td>False</td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-settings">settings</h3>
<div class="attribute-type-info">object</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

A map containing additional settings.  Each map entry has a
string name and a string value.

**Note:** In general, we recommend not changing settings from
their default values.


- `observer`: Set the protocol observer used to generate
  traffic metrics.<br/>
  Default: `auto`. Choices: `auto`, `none`, `http1`, `http2`.



</div>
</div>

## Status properties

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-status">status</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The current state of the resource.

- `Pending`: The resource is being processed.
- `Error`: There was an error processing the resource.  See
  `message` for more information.
- `Ready`: The resource is ready to use.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-message">message</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

A human-readable status message.  Error messages are reported
here.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-has-destination">hasDestination</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

True if there is at least one connector in the network with a
routing key matched by the strategy.

<table class="fields"><tr><th>Default</th><td>False</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-strategy">strategy</h3>
<div class="attribute-type-info">object</div>
</div>
<div class="attribute-body">

Current state of the routing strategy, including which routing
keys are reachable.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-strategy.priority">strategy.priority</h3>
<div class="attribute-type-info">None</div>
</div>
<div class="attribute-body">

Priority strategy status information.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-strategy.priority.routing-keys-reachable">strategy.priority.routingKeysReachable</h3>
<div class="attribute-type-info">array</div>
</div>
<div class="attribute-body">

List of routing keys with at least one reachable connector,
given in priority order.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-strategy.weighted">strategy.weighted</h3>
<div class="attribute-type-info">None</div>
</div>
<div class="attribute-body">

Weighted strategy status information.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-strategy.weighted.routing-keys-reachable">strategy.weighted.routingKeysReachable</h3>
<div class="attribute-type-info">object</div>
</div>
<div class="attribute-body">

Mapping of routing keys to weights for keys with at least one
reachable connector.



</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="status-conditions">conditions</h3>
<div class="attribute-type-info">array</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

A set of named conditions describing the current state of the
resource.


- `Configured`: The multi-key listener configuration has been applied
  to the router.
- `Operational`: There is at least one connector corresponding to
  the multi-key listener strategy.
- `Ready`: The multi-key listener is ready to use. All other conditions
  are true.

<table class="fields"><tr><th>See also</th><td><a href="https://maelvls.dev/kubernetes-conditions/">Kubernetes conditions</a></td></table>

</div>
</div>
