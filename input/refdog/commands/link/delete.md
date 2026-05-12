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

# Link delete command

~~~ shell
skupper link delete [options]
~~~

Delete a link by name

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td><tr><th>Waits for</th><td>Deletion</td></table>

## Examples

~~~ console
# Delete a link
$ skupper link delete west-6bfn6
Waiting for deletion...
Link "west-6bfn6" is deleted.
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for delete



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
<h3 id="option-wait">--wait</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

Wait for deletion to complete before exiting (default true) ``` ``` -c, --context string      Set the kubeconfig context

<table class="fields"><tr><th>Default</th><td><p><code>true</code></p>
</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-kubeconfig">--kubeconfig</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

Path to the kubeconfig file to use -n, --namespace string    Set the namespace -p, --platform string     Set the platform type to use [kubernetes, podman, docker, linux] ```



</div>
</div>

## Global options
