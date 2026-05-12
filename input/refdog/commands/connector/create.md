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

The hostname or IP address of the local connector



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-include-not-ready">--include-not-ready</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

If true, include server pods that are not in the ready state. -r, --routing-key string       The identifier used to route traffic from listeners to connectors



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-selector">--selector</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

A Kubernetes label selector for specifying target server pods.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-timeout">--timeout</h3>
<div class="attribute-type-info">&lt;duration&gt;</div>
</div>
<div class="attribute-body">

raise an error if the operation does not complete in the given period of time (expressed in seconds). (default 1m0s)

<table class="fields"><tr><th>Default</th><td><p><code>1m0s</code></p>
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

The connector type. Choices: [tcp]. (default "tcp")

<table class="fields"><tr><th>Default</th><td><p><code>&quot;tcp&quot;</code></p>
</td><tr><th>Choices</th><td><table class="choices"><tr><th><code>tcp</code></th><td></td></tr></table></td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-wait">--wait</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

Wait for the given status before exiting. Choices: configured, ready, none (default "configured")

<table class="fields"><tr><th>Default</th><td><p><code>&quot;configured&quot;</code></p>
</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-workload">--workload</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

A Kubernetes resource name that identifies a workload expressed like resource-type/resource-name. Expected resource types: service, daemonset, deployment, and statefulset. ``` ``` -c, --context string      Set the kubeconfig context



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
