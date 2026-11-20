---
body_class: object command
refdog_links: []
refdog_object_has_attributes: true
render_macros: false
---

# Debug conn command

~~~ shell
skupper debug conn [options]
~~~

Queries the router management API for TCP adaptor connections, correlates
them with listener/connector resources (routing key, resource name), and lists
matching connections (idle time, TCP state, routing key). Connections idle
beyond --idle-threshold can be force-closed with --execute via
adminStatus=deleted.
With --list-ports it instead reports how many connections each port carries,
inbound and outbound, plus the correlated routing key and resource, and closes
nothing.
--port, --state, --routing-key, and --kind narrow either mode. --port is the
router-side port shown by --list-ports (on Kubernetes this is often an
allocated port such as 1024, not Listener spec.port). Note that closing a
connection also closes the other leg of its flow, which sits on the
connector's port and so may differ from the port swept.
"sweep" remains as an alias for compatibility.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Examples

~~~ console
# List all connections
$ skupper debug conn

# List ports with connection counts
$ skupper debug conn --list-ports

# Filter by TCP state and routing key
$ skupper debug conn --state ESTAB --routing-key echo:8080

# Close idle connections matching filters
$ skupper debug conn --port 1024 --idle-threshold 14400 --execute
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-execute">--execute</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

Close idle connections matching the filters; without this flag matching connections are listed



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for conn



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-idle-threshold">--idle-threshold</h3>
<div class="attribute-type-info">&lt;int&gt;</div>
</div>
<div class="attribute-body">

Seconds with no data received before a connection is flagged as orphaned (default 14400)

<table class="fields"><tr><th>Default</th><td><p><code>14400</code></p>
</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-kind">--kind</h3>
<div class="attribute-type-info">&lt;strings&gt;</div>
</div>
<div class="attribute-body">

Only consider connections correlated to this resource kind (listener, connector, multikeylistener); repeat or comma-separate



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-list-ports">--list-ports</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

List each port in use with its inbound and outbound connection counts, instead of sweeping



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-output">--output</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

Output format: text or json (default "text")

<table class="fields"><tr><th>Default</th><td><p><code>&quot;text&quot;</code></p>
</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-port">--port</h3>
<div class="attribute-type-info">&lt;ints&gt;</div>
</div>
<div class="attribute-body">

Only consider connections on this router-side port (see --list-ports); repeat the flag for several ports (default: all ports)

<table class="fields"><tr><th>Default</th><td><p><code>all ports</code></p>
</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-routing-key">--routing-key</h3>
<div class="attribute-type-info">&lt;strings&gt;</div>
</div>
<div class="attribute-body">

Only consider connections correlated to this routing key; repeat or comma-separate



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-state">--state</h3>
<div class="attribute-type-info">&lt;strings&gt;</div>
</div>
<div class="attribute-body">

Only consider connections whose kernel socket is in this TCP state (ss names: ESTAB, FIN-WAIT-2, …); repeat or comma-separate ``` ``` -n, --namespace string   Set the namespace -p, --platform string    Set the platform type to use [kubernetes, podman, docker, linux] ```



</div>
</div>

## Global options
