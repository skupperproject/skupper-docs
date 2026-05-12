---
body_class: object command
refdog_links:
- title: Site configuration
  url: /docs/refdog/topics/site-configuration.html
- title: Site concept
  url: /docs/refdog/concepts/site.html
- title: Site resource
  url: /docs/refdog/resources/site.html
refdog_object_has_attributes: true
render_macros: false
---

# Site delete command

~~~ shell
skupper site delete [options]
~~~

Delete a site

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td><tr><th>Waits for</th><td>Deletion</td></table>

## Examples

~~~ console
# Delete the current site
$ skupper site delete
Waiting for deletion...
Site "west" is deleted.

# Delete the current site and all of its associated Skupper resources
$ skupper site delete --all
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-all">--all</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

delete all skupper resources associated with site in current namespace



</div>
</div>

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

## Errors

- **No site resource exists**

  <p>There is no existing Skupper site resource to delete.</p>
