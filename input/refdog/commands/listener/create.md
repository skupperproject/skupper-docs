---
body_class: object command
refdog_links:
- title: Service exposure
  url: /docs/refdog/topics/service-exposure.html
- title: Listener concept
  url: /docs/refdog/concepts/listener.html
- title: Listener resource
  url: /docs/refdog/resources/listener.html
- title: Connector create command
  url: /docs/refdog/commands/connector/create.html
- title: Connector command
  url: /docs/refdog/commands/connector/index.html
refdog_object_has_attributes: true
render_macros: false
---

# Listener create command

~~~ shell
skupper listener create [options]
~~~

Clients at this site use the listener host and port to establish connections to the remote service.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td><tr><th>Waits for</th><td>Configured</td></table>

## Examples

~~~ console
# Create a listener for a database
$ skupper listener create database 5432
Waiting for status...
Listener "database" is configured.

# Set the routing key and host explicitly
$ skupper listener create backend 8080 --routing-key be1 --host apiserver
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for create



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-host">--host</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

The hostname or IP address of the local listener. Clients at this site use the listener host and port to establish connections to the remote service.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-routing-key">--routing-key</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

The identifier used to route traffic from listeners to connectors



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-tls-credentials">--tls-credentials</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

the name of a Kubernetes secret containing the generated or externally-supplied TLS credentials.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-type">--type</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

The listener type. Choices: [tcp]. (default "tcp") ``` ``` -n, --namespace string   Set the namespace -p, --platform string    Set the platform type to use [kubernetes, podman, docker, linux] ```

<table class="fields"><tr><th>Default</th><td><p><code>&quot;tcp&quot;</code></p>
</td><tr><th>Choices</th><td><table class="choices"><tr><th><code>tcp</code></th><td></td></tr></table></td></table>

</div>
</div>

## Global options
