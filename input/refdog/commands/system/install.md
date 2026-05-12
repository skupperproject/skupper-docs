---
body_class: object command
refdog_links:
- title: Platform concept
  url: /docs/refdog/concepts/platform.html
- title: System uninstall command
  url: /docs/refdog/commands/system/uninstall.html
refdog_object_has_attributes: true
render_macros: false
---

# System install command

~~~ shell
skupper system install [options]
~~~

Checks the local environment for required resources and configuration.
In some instances, configures the local environment. It starts the Podman/Docker API 
service if it is not already available.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for install



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-reload-type">--reload-type</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

Specify the type of reload to perform. Choices: manual, auto (default "manual") ``` ``` -c, --context string      Set the kubeconfig context

<table class="fields"><tr><th>Default</th><td><p><code>&quot;manual&quot;</code></p>
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
