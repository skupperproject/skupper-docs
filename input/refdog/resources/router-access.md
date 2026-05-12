---
body_class: object resource
refdog_links:
- title: Site linking
  url: /docs/refdog/topics/site-linking.html
- title: Site resource
  url: /docs/refdog/resources/site.html
- title: Link resource
  url: /docs/refdog/resources/link.html
refdog_object_has_attributes: true
render_macros: false
---

# RouterAccess resource

Configuration for secure access to the site router.  The
configuration includes TLS credentials and router ports.  The
RouterAccess resource is used to implement link access for sites.

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
<h3 id="spec-roles">roles</h3>
<div class="attribute-type-info">array</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The named interfaces by which a router can be accessed.  These
include "inter-router" for links between interior routers and
"edge" for links from edge routers to interior routers.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-tls-credentials">tlsCredentials</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The name of a bundle of TLS certificates used for mutual TLS
router-to-router communication.  The bundle contains the
server certificate and key and the trusted client certificate
(usually a CA).

On Kubernetes, the value is the name of a Secret in the
current namespace.

On Docker, Podman, and Linux, the value is the name of a
directory under `input/certs/` in the current namespace.

<table class="fields"><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets">Kubernetes TLS secrets</a></td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-generate-tls-credentials">generateTlsCredentials</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

When set, Skupper generates the TLS credentials to be
stored in the Secret specified by `tlsCredentials`. See
also `issuer`.

<table class="fields"><tr><th>Default</th><td>False</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-issuer">issuer</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The name of the Kubernetes Secret containing the signing CA
used to generate TLS certificates for the RouterAccess when
`generateTlsCredentials` is set.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-access-type">accessType</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

Configures the access type for the router endpoints.
Available access types and the default selection is
configured on the Skupper controller for Kubernetes.

The options available by default are:
  - `local`: No external ingress. Implies a Kubernetes Service with type CluterIP.
  - `route`: Exposed via an OpenShift Route.
  - `loadbalancer`: Exposed via a Kubernetes Service with type LoadBalancer.

<table class="fields"><tr><th>Default</th><td><p><em>On OpenShift, the default is <code>route</code>.  For other
Kubernetes flavors, the default is <code>loadbalancer</code>.</em></p>
</td><tr><th>Choices</th><td><table class="choices"><tr><th><code>route</code></th><td><p>Use an OpenShift route.  <em>OpenShift only.</em></p>
</td></tr><tr><th><code>loadbalancer</code></th><td><p>Use a Kubernetes load balancer.</p>
</td></tr></table></td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-bind-host">bindHost</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The hostname or IP address of the network interface to bind
to.  By default, Skupper binds all the interfaces on the host.

<table class="fields"><tr><th>Default</th><td><p><code>0.0.0.0</code></p>
</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-subject-alternative-names">subjectAlternativeNames</h3>
<div class="attribute-type-info">array</div>
</div>
<div class="attribute-body">

The hostnames and IPs secured by the router TLS certificate.

<table class="fields"><tr><th>Default</th><td><p><em>The current hostname and the IP address of each bound network
interface</em></p>
</td></table>

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

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="status-conditions">conditions</h3>
<div class="attribute-type-info">array</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

A set of named conditions describing the current state of the
resource.


- `Configured`: The router access configuration has been applied to
  the router.
- `Resolved`: The connection endpoints are available.
- `Ready`: The router access is ready to use.  All other
  conditions are true.

<table class="fields"><tr><th>See also</th><td><a href="https://maelvls.dev/kubernetes-conditions/">Kubernetes conditions</a></td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="status-endpoints">endpoints</h3>
<div class="attribute-type-info">array</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

An array of connection endpoints.  Each item has a name, host,
port, and group.



</div>
</div>
