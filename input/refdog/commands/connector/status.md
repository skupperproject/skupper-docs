---
body_class: object command
refdog_links:
- title: Service exposure
  url: /docs/refdog/topics/service-exposure.html
- title: Connector concept
  url: /docs/refdog/concepts/connector.html
- title: Connector resource
  url: /docs/refdog/resources/connector.html
- title: Listener status command
  url: /docs/refdog/commands/listener/status.html
- title: Listener command
  url: /docs/refdog/commands/listener/index.html
refdog_object_has_attributes: true
render_macros: false
---

# Connector status command

~~~ shell
skupper connector status [options]
~~~

Display status of all connectors or a specific connector

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Examples

~~~ console
# Show the status of all connectors in the current site
$ skupper connector status
NAME       STATUS   ROUTING-KEY   SELECTOR         HOST     PORT   LISTENERS
backend    Ready    backend       app=backend      <none>   8080   true
database   Ready    database      app=postgresql   <none>   5432   true

# Show the status of one connector
$ skupper connector status backend
Name:                     backend
Status:                   Ready
Message:                  <none>
Routing key:              backend
Selector:                 app=backend
Host:                     <none>
Port:                     8080
Has matching listeners:   1
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for status -o, --output string   print status of connectors Choices: json, yaml ``` ``` -n, --namespace string   Set the namespace -p, --platform string    Set the platform type to use [kubernetes, podman, docker, linux] ```



</div>
</div>

## Global options
