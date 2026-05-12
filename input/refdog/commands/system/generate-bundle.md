---
body_class: object command
refdog_links:
- title: Platform concept
  url: /docs/refdog/concepts/platform.html
refdog_object_has_attributes: true
render_macros: false
---

# System generate-bundle command

~~~ shell
skupper system generate-bundle [options]
~~~

Generate a self-contained site bundle for use on another machine.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for generate-bundle



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-input">--input</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

The location of the Skupper resources defining the site.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-type">--type</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

The bundle type to be produced. Choices: tarball, shell-script (default "tarball") ``` ``` -c, --context string      Set the kubeconfig context

<table class="fields"><tr><th>Default</th><td><p><code>&quot;tarball&quot;</code></p>
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
