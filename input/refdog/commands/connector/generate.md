---
body_class: object command
refdog_links:
- title: Service exposure
  url: /docs/refdog/topics/service-exposure.html
- title: Connector concept
  url: /docs/refdog/concepts/connector.html
- title: Connector resource
  url: /docs/refdog/resources/connector.html
- title: Listener generate command
  url: /docs/refdog/commands/listener/generate.html
- title: Listener command
  url: /docs/refdog/commands/listener/index.html
refdog_object_has_attributes: true
render_macros: false
---

# Connector generate command

~~~ shell
skupper connector generate [options]
~~~

Clients at this site use the connector host and port to establish connections to the remote service.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Examples

~~~ console
# Generate a Connector resource and print it to the console
$ skupper connector generate backend 8080
apiVersion: skupper.io/v2alpha1
kind: Connector
metadata:
  name: backend
spec:
  routingKey: backend
  port: 8080
  selector: app=backend

# Generate a Connector resource and direct the output to a file
$ skupper connector generate backend 8080 > backend.yaml
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for generate



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

If true, include server pods that are not in the ready state. -o, --output string            print resources to the console instead of submitting them to the Skupper controller. Choices: json, yaml (default "yaml")

<table class="fields"><tr><th>Default</th><td><p><code>&quot;yaml&quot;</code></p>
</td></table>

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
<h3 id="option-selector">--selector</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

A Kubernetes label selector for specifying target server pods.



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
