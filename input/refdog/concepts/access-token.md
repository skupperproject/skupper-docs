---
body_class: object concept
refdog_links:
- title: Site linking
  url: /docs/refdog/topics/site-linking.html
- title: AccessToken resource
  url: /docs/refdog/resources/access-token.html
- title: Link concept
  url: /docs/refdog/concepts/link.html
- title: AccessGrant resource
  url: /docs/refdog/resources/access-grant.html
- title: AccessToken resource
  url: /docs/refdog/resources/access-token.html
- title: Token command
  url: /docs/refdog/commands/token/index.html
render_macros: false
---

# Access token concept

An access token is a short-lived credential used to create a
[link](link.html).  An access token contains the URL and secret code
of a corresponding _access grant_.

<figure>
  <img src="images/access-token-model-1.svg"/>
  <figcaption>Issuing tokens</figcaption>
</figure>

<figure>
  <img src="images/access-token-model-2.svg"/>
  <figcaption>Redeeming tokens</figcaption>
</figure>

Access tokens are issued from access grants.  A grant issues zero or
more tokens.  Tokens are redeemed for links.

Access tokens have limited redemptions and limited lifespans.
By default, they can be redeemed only once, and they expire 15
minutes after being issued.  You can set custom limits by
configuring the access grant.

<figure>
  <img src="images/access-token-1.svg" style="max-height: 40em;"/>
  <figcaption>The sequence for issuing and redeeming access tokens</figcaption>
</figure>

* A site wishing to accept a link (site 1) creates an access grant.

* It uses the access grant to issue a corresponding access token
  and transfers it to a remote site (site 2).

* Site 2 submits the access token to site 1 for redemption.

* If the token is valid, site 1 sends site 2 the TLS host, port, and
  credentials required to create a link to site 1.
