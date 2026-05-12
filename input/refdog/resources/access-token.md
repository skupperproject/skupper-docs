---
body_class: object resource
refdog_links:
- title: Site linking
  url: /docs/refdog/topics/site-linking.html
- title: Access token concept
  url: /docs/refdog/concepts/access-token.html
- title: Access token concept
  url: /docs/refdog/concepts/access-token.html
- title: AccessGrant resource
  url: /docs/refdog/resources/access-grant.html
- title: Token issue command
  url: /docs/refdog/commands/token/issue.html
- title: Token redeem command
  url: /docs/refdog/commands/token/redeem.html
refdog_object_has_attributes: true
render_macros: false
---

# AccessToken resource

A short-lived credential used to create a link.  An access token
contains the URL and secret code of a corresponding access grant.

**Note:** Access tokens are often [issued][issue] and
[redeemed][redeem] using the Skupper CLI.

[issue]: /docs/refdog/commands/token/issue.html
[redeem]: /docs/refdog/commands/token/redeem.html

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
<h3 id="spec-url">url</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The URL of the grant service at the remote site.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-code">code</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The secret code used to authenticate the token when
submitted for redemption.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-ca">ca</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The trusted server certificate of the grant service at the
remote site.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-link-cost">linkCost</h3>
<div class="attribute-type-info">integer</div>
</div>
<div class="attribute-body">

The link cost to use when creating the link.

<table class="fields"><tr><th>Default</th><td>1</td></table>

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
<h3 id="status-redeemed">redeemed</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

True if the token has been redeemed.  Once a token is
redeemed, it cannot be used again.

<table class="fields"><tr><th>Default</th><td>False</td></table>

</div>
</div>

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


- `Redeemed`: The token has been exchanged for a link.

<table class="fields"><tr><th>See also</th><td><a href="https://maelvls.dev/kubernetes-conditions/">Kubernetes conditions</a></td></table>

</div>
</div>
