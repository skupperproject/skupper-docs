---
body_class: object command
refdog_links:
- title: Platform concept
  url: /docs/refdog/concepts/platform.html
- title: System stop command
  url: /docs/refdog/commands/system/stop.html
refdog_object_has_attributes: true
render_macros: false
---

# System start command

~~~ shell
skupper system start [options]
~~~

Start the Skupper router for the current site. This starts the systemd service for the current namespace.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for start ``` ``` -n, --namespace string   Set the namespace -p, --platform string    Set the platform type to use [kubernetes, podman, docker, linux] ```



</div>
</div>

## Global options
