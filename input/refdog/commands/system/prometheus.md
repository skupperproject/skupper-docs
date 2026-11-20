---
body_class: object command
refdog_links:
- title: Platform concept
  url: /docs/refdog/concepts/platform.html
refdog_object_has_attributes: true
render_macros: false
---

# System prometheus command

~~~ shell
skupper system prometheus [options]
~~~

Install a single Prometheus container shared by all network observers on this host.
This must be run before installing any network observer.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for prometheus



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-uninstall">--uninstall</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

Uninstall Prometheus ``` ``` -n, --namespace string   Set the namespace -p, --platform string    Set the platform type to use [kubernetes, podman, docker, linux] ```



</div>
</div>

## Global options
