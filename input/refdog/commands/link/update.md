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

# Link update command

~~~ shell
skupper link update [options]
~~~

Change link settings

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td><tr><th>Waits for</th><td>Ready</td></table>

## Examples

~~~ console
# Change the link cost
$ skupper link update west-6bfn6 --cost 10
Waiting for status...
Link "west-6bfn6" is ready.
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
</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for update



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-timeout">--timeout</h3>
<div class="attribute-type-info">&lt;duration&gt;</div>
</div>
<div class="attribute-body">

raise an error if the operation does not complete in the given period of time (expressed in seconds). (default 1m0s)

<table class="fields"><tr><th>Default</th><td><p><code>1m0s</code></p>
</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-tls-credentials">--tls-credentials</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

the name of a Kubernetes secret containing the generated or externally-supplied TLS credentials. ``` ``` -n, --namespace string   Set the namespace -p, --platform string    Set the platform type to use [kubernetes, podman, docker, linux] ```



</div>
</div>

## Global options
