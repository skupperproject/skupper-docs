---
body_class: object resource
refdog_links:
- title: Site linking
  url: /docs/refdog/topics/site-linking.html
- title: Access token concept
  url: /docs/refdog/concepts/access-token.html
- title: AccessToken resource
  url: /docs/refdog/resources/access-token.html
- title: Token issue command
  url: /docs/refdog/commands/token/issue.html
refdog_object_has_attributes: true
render_macros: false
---

# AccessGrant resource

Permission to redeem access tokens for links to the local
site.  A remote site can use a token containing the grant
URL and secret code to obtain a certificate signed by the
grant's certificate authority (CA), within a certain
expiration window and for a limited number of redemptions.

The `code`, `url`, and `ca` properties of the resource
status are used to generate access tokens from the grant.

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
<h3 id="spec-redemptions-allowed">redemptionsAllowed</h3>
<div class="attribute-type-info">integer</div>
</div>
<div class="attribute-body">

The number of times an access token for this grant can
be redeemed.

<table class="fields"><tr><th>Default</th><td>1</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="spec-expiration-window">expirationWindow</h3>
<div class="attribute-type-info">string (duration)</div>
</div>
<div class="attribute-body">

The period of time in which an access token for this
grant can be redeemed.

<table class="fields"><tr><th>Default</th><td><p><code>15m</code></p>
</td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-code">code</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

The secret code to use to authenticate access tokens submitted
for redemption.

If not set, a value is generated and placed in the `code`
status property.



</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="spec-issuer">issuer</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">advanced</div>
</div>
<div class="attribute-body">

The name of a Kubernetes secret used to generate a
certificate when redeeming a token for this grant.

If not set, `defaultIssuer` on the Site rsource is used.

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
<h3 id="status-redemptions">redemptions</h3>
<div class="attribute-type-info">integer</div>
</div>
<div class="attribute-body">

The number of times a token for this grant has been
redeemed.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-expiration-time">expirationTime</h3>
<div class="attribute-type-info">string (date-time)</div>
</div>
<div class="attribute-body">

The point in time when the grant expires.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-url">url</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The URL of the token-redemption service for this grant.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-ca">ca</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The trusted server certificate of the token-redemption
service for this grant.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="status-code">code</h3>
<div class="attribute-type-info">string</div>
</div>
<div class="attribute-body">

The secret code used to authenticate access tokens
submitted for redemption.

<table class="fields"><tr><th>Default</th><td><p><em>Generated</em></p>
</td></table>

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


- `Processed`: The controller has accepted the grant.
- `Resolved`: The grant service is available to process tokens
  for this grant.
- `Ready`: The grant is ready to use.  All other
  conditions are true.

<table class="fields"><tr><th>See also</th><td><a href="https://maelvls.dev/kubernetes-conditions/">Kubernetes conditions</a></td></table>

</div>
</div>
