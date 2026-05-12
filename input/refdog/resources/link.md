---
body_class: object resource
refdog_links:
- title: Site linking
  url: /docs/refdog/topics/site-linking.html
- title: Link concept
  url: /docs/refdog/concepts/link.html
- title: Link command
  url: /docs/refdog/commands/link/index.html
- title: AccessToken resource
  url: /docs/refdog/resources/access-token.html
refdog_object_has_attributes: true
render_macros: false
---

# Link resource

A link is a channel for communication between [sites](site.html).
Links carry application connections and requests.  A set of linked
sites constitutes a network.

A Link resource specifies remote connection endpoints and TLS
credentials for establishing a mutual TLS connection to a remote
site.  To create an active link, the remote site must first enable
_link access_.  Link access provides an external access point for
accepting links.

**Note:** Links are not usually created directly.  Instead, you can
use an [access token][token] to obtain a link.

[token]: access-token.html

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
<h3 id="spec-endpoints">endpoints</h3>
<div class="attribute-type-info">array</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

An array of connection endpoints. Each item has a name, host,
port, and group.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-cost">cost</h3>
<div class="attribute-type-info">integer</div>
</div>
<div class="attribute-body">

The configured routing cost of sending traffic over
the link.

<table class="fields"><tr><th>Default</th><td>1</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-tls-credentials">tlsCredentials</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The name of a bundle of certificates used for mutual TLS
router-to-router communication.  The bundle contains the
client certificate and key and the trusted server certificate
(usually a CA).

On Kubernetes, the value is the name of a Secret in the
current namespace.

On Docker, Podman, and Linux, the value is the name of a
directory under `input/certs/` in the current namespace.

<table class="fields"><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets">Kubernetes TLS secrets</a></td></table>

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

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-remote-site-id">remoteSiteId</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The unique ID of the site linked to.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-remote-site-name">remoteSiteName</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The name of the site linked to.



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


- `Configured`: The link configuration has been applied to
  the router.
- `Operational`: The link to the remote site is active.
- `Ready`: The link is ready to use.  All other conditions
  are true.

<table class="fields"><tr><th>See also</th><td><a href="https://maelvls.dev/kubernetes-conditions/">Kubernetes conditions</a></td></table>

</div>
</div>
