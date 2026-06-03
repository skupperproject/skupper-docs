---
body_class: object command
refdog_links:
- title: Service exposure
  url: /docs/refdog/topics/service-exposure.html
- title: Listener concept
  url: /docs/refdog/concepts/listener.html
- title: Listener resource
  url: /docs/refdog/resources/listener.html
- title: Connector update command
  url: /docs/refdog/commands/connector/update.html
- title: Connector command
  url: /docs/refdog/commands/connector/index.html
refdog_object_has_attributes: true
render_macros: false
---

# Listener update command

~~~ shell
skupper listener update [options]
~~~

Clients at this site use the listener host and port to establish connections to the remote service.
	The user can change port, host name, TLS credentials, listener type and routing key

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td><tr><th>Waits for</th><td>Configured</td></table>

## Examples

~~~ console
# Change the host and port
$ skupper listener update database --host mysql --port 3306
Waiting for status...
Listener "database" is configured.

# Change the routing key
$ skupper listener update backend --routing-key be2
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for update



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
<h3 id="option-port">--port</h3>
<div class="attribute-type-info">&lt;int&gt;</div>
</div>
<div class="attribute-body">

The port of the local listener



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
