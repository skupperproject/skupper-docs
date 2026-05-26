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

help for delete ``` ``` -n, --namespace string   Set the namespace -p, --platform string    Set the platform type to use [kubernetes, podman, docker, linux] ```



</div>
</div>

## Global options

## Errors

- **No site resource exists**

  <p>There is no existing Skupper site resource to delete.</p>
