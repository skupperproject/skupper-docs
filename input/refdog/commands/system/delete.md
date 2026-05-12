---
body_class: object command
refdog_links:
- title: Platform concept
  url: /docs/refdog/concepts/platform.html
refdog_object_has_attributes: true
render_macros: false
---

# System delete command

~~~ shell
skupper system delete [options]
~~~

Delete resources using files or standard input.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for delete ``` ``` -c, --context string      Set the kubeconfig context



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
