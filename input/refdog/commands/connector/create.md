---
body_class: object command
refdog_links:
- title: Service exposure
  url: /docs/refdog/topics/service-exposure.html
- title: Connector concept
  url: /docs/refdog/concepts/connector.html
- title: Connector resource
  url: /docs/refdog/resources/connector.html
- title: Listener create command
  url: /docs/refdog/commands/listener/create.html
- title: Listener command
  url: /docs/refdog/commands/listener/index.html
refdog_object_has_attributes: true
render_macros: false
---

# Connector create command

~~~ shell
skupper connector create [options]
~~~

Clients at this site use the connector host and port to establish connections to the remote service.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td><tr><th>Waits for</th><td>Configured</td></table>

## Examples

~~~ console
# Create a connector for a database
$ skupper connector create database 5432
Waiting for status...
Connector "database" is configured.

# Set the routing key and selector explicitly
$ skupper connector create backend 8080 --routing-key be1 --selector app=be1

# Use the workload option to select pods
$ skupper connector create backend 8080 --workload deployment/backend
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

The hostname or IP address of the local connector (default "localhost") -r, --routing-key string       The identifier used to route traffic from listeners to connectors

<table class="fields"><tr><th>Default</th><td><p><code>&quot;localhost&quot;</code></p>
</td></table>

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

The connector type. Choices: [tcp]. (default "tcp") ``` ``` -n, --namespace string   Set the namespace -p, --platform string    Set the platform type to use [kubernetes, podman, docker, linux] ```

<table class="fields"><tr><th>Default</th><td><p><code>&quot;tcp&quot;</code></p>
</td><tr><th>Choices</th><td><table class="choices"><tr><th><code>tcp</code></th><td></td></tr></table></td></table>

</div>
</div>

## Global options
