---
body_class: object command
refdog_links:
- title: Site linking
  url: /docs/refdog/topics/site-linking.html
- title: Access token concept
  url: /docs/refdog/concepts/access-token.html
- title: AccessGrant resource
  url: /docs/refdog/resources/access-grant.html
- title: AccessToken resource
  url: /docs/refdog/resources/access-token.html
- title: Token redeem command
  url: /docs/refdog/commands/token/redeem.html
refdog_object_has_attributes: true
render_macros: false
---

# Token issue command

~~~ shell
skupper token issue [options]
~~~

Issue a token file redeemable for a link to the current site.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes</td><tr><th>Waits for</th><td>Ready</td></table>

## Examples

~~~ console
# Issue an access token
$ skupper token issue ~/token.yaml
Waiting for status...
Access grant "west-6bfn6" is ready.
Token file /home/fritz/token.yaml created.

Transfer this file to a remote site. At the remote site,
create a link to this site using the 'skupper token
redeem' command:

    $ skupper token redeem <file>

The token expires after 1 use or after 15 minutes.

# Issue an access token with non-default limits
$ skupper token issue ~/token.yaml --expiration-window 24h --redemptions-allowed 3

# Issue a token using an existing access grant
$ skupper token issue ~/token.yaml --grant west-1
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-cost">--cost</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

the configured "expense" of sending traffic over the link. (default "1")

<table class="fields"><tr><th>Default</th><td><p><code>&quot;1&quot;</code></p>
</td><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-expiration-window">--expiration-window</h3>
<div class="attribute-type-info">&lt;duration&gt;</div>
</div>
<div class="attribute-body">

The period of time in which an access token for this grant can be redeemed. (default 15m0s)

<table class="fields"><tr><th>Default</th><td><p><code>15m0s</code></p>
</td><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for issue

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-redemptions-allowed">--redemptions-allowed</h3>
<div class="attribute-type-info">&lt;int&gt;</div>
</div>
<div class="attribute-body">

The number of times an access token for this grant can be redeemed. (default 1)

<table class="fields"><tr><th>Default</th><td><p><code>1</code></p>
</td><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-timeout">--timeout</h3>
<div class="attribute-type-info">&lt;duration&gt;</div>
</div>
<div class="attribute-body">

raise an error if the operation does not complete in the given period of time (expressed in seconds). (default 1m0s) ``` ``` -n, --namespace string   Set the namespace -p, --platform string    Set the platform type to use [kubernetes, podman, docker, linux] ```

<table class="fields"><tr><th>Default</th><td><p><code>1m0s</code></p>
</td><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

</div>
</div>

## Global options

## Errors

- **Link access is not enabled**

  <p>Link access at this site is not currently enabled.  You
can use "skupper site update --enable-link-access" to
enable it.</p>
