---
body_class: object command
refdog_links:
- title: Platform concept
  url: /docs/refdog/concepts/platform.html
refdog_object_has_attributes: true
render_macros: false
---

# System network-observer command

~~~ shell
skupper system network-observer [options]
~~~

Install the Skupper network observer to collect and expose network metrics.
The network observer requires an existing Skupper site and will deploy two containers:
- network-observer: Collects metrics from the router
- prometheus: Stores metrics

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for network-observer



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-uninstall">--uninstall</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

Uninstall Network Observer ``` ``` -n, --namespace string   Set the namespace -p, --platform string    Set the platform type to use [kubernetes, podman, docker, linux] ```



</div>
</div>

## Global options
