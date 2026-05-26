---
body_class: object command
refdog_links:
- title: Site linking
  url: /docs/refdog/topics/site-linking.html
- title: Link concept
  url: /docs/refdog/concepts/link.html
- title: Link resource
  url: /docs/refdog/resources/link.html
- title: Token command
  url: /docs/refdog/commands/token/index.html
refdog_object_has_attributes: true
render_macros: false
---

# Link command

~~~ shell
skupper link [subcommand] [options]
~~~

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Subcommands

<table class="objects">
<tr><th><a href="/docs/refdog/commands/link/update.html">Link update</a></th><td>Change link settings
</td></tr>
<tr><th><a href="/docs/refdog/commands/link/delete.html">Link delete</a></th><td>Delete a link by name
</td></tr>
<tr><th><a href="/docs/refdog/commands/link/status.html">Link status</a></th><td>Display the status of links in the current site</td></tr>
<tr><th><a href="/docs/refdog/commands/link/generate.html">Link generate</a></th><td>Generate a new link resource as a YAML output The resultant output needs to be applied in the site in which we want to create the link</td></tr>
</table>
