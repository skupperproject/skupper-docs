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
refdog_object_has_attributes: true
render_macros: false
---

# Token command

~~~ shell
skupper token [subcommand] [options]
~~~

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Subcommands

<table class="objects">
<tr><th><a href="/docs/refdog/commands/token/issue.html">Token issue</a></th><td>Issue a token file redeemable for a link to the current site</td></tr>
<tr><th><a href="/docs/refdog/commands/token/redeem.html">Token redeem</a></th><td>Redeem a token file in order to create a link to a remote site</td></tr>
</table>
