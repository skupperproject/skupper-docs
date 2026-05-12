---
body_class: object command
refdog_links:
- title: Service exposure
  url: /docs/refdog/topics/service-exposure.html
- title: Listener concept
  url: /docs/refdog/concepts/listener.html
- title: Listener resource
  url: /docs/refdog/resources/listener.html
- title: Connector status command
  url: /docs/refdog/commands/connector/status.html
- title: Connector command
  url: /docs/refdog/commands/connector/index.html
refdog_object_has_attributes: true
render_macros: false
---

# Listener status command

~~~ shell
skupper listener status [options]
~~~

Display status of all listeners or a specific listener

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Examples

~~~ console
# Show the status of all listeners in the current site
$ skupper listener status
NAME       STATUS   ROUTING-KEY   HOST       PORT   CONNECTORS
backend    Ready    backend       backend    8080   true
database   Ready    database      database   5432   true

# Show the status of one listener
$ skupper listener status backend
Name:                      backend
Status:                    Ready
Message:                   <none>
Routing key:               backend
Host:                      backend
Port:                      8080
Has matching connectors:   true
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for status -o, --output string   print resources to the console instead of submitting them to the Skupper controller. Choices: json, yaml ``` ``` -c, --context string      Set the kubeconfig context



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
