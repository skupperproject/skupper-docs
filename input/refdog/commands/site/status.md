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

# Site status command

~~~ shell
skupper site status [options]
~~~

Display the current status of a site.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Examples

~~~ console
# Show the status of the current site
$ skupper site status
Name:      west
Status:    Ready
Message:   -
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for status -o, --output string   print status of connectors Choices: json, yaml ``` ``` -c, --context string      Set the kubeconfig context



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
