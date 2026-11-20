---
body_class: object command
refdog_links: []
refdog_object_has_attributes: true
render_macros: false
---

# Debug command

~~~ shell
skupper debug [subcommand] [options]
~~~

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Subcommands

<table class="objects">
<tr><th><a href="/docs/refdog/commands/debug/cert-inspect.html">Debug cert-inspect</a></th><td>Decode and display key fields of X.509 certificates managed by Skupper, including subject, issuer, validity period, SANs, and public key information</td></tr>
<tr><th><a href="/docs/refdog/commands/debug/conn.html">Debug conn</a></th><td>Queries the router management API for TCP adaptor connections, correlates them with listener/connector resources (routing key, resource name), and lists matching connections (idle time, TCP state, routing key)</td></tr>
<tr><th><a href="/docs/refdog/commands/debug/dump.html">Debug dump</a></th><td>Create a tarball including site resources and status; component versions, config files,  	and logs; and info about the environment where Skupper is running
</td></tr>
</table>
