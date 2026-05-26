---
body_class: object command
refdog_links:
- title: Site linking
  url: /docs/refdog/topics/site-linking.html
- title: Link concept
  url: /docs/refdog/concepts/link.html
- title: Link resource
  url: /docs/refdog/resources/link.html
- title: Token command
  url: /docs/refdog/commands/token/index.html
refdog_object_has_attributes: true
render_macros: false
---

# Link generate command

~~~ shell
skupper link generate [options]
~~~

Generate a new link resource as a YAML output The resultant
output needs to be applied in the site in which we want to create the link.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td><tr><th>Waits for</th><td>Site resource ready</td></table>

## Examples

~~~ console
# Generate a Link resource and print it to the console
$ skupper link generate
apiVersion: skupper.io/v2alpha1
kind: Link
metadata:
  name: south-ac619
spec:
  endpoints:
    - group: skupper-router-1
      host: 10.97.161.185
      name: inter-router
      port: "55671"
    - group: skupper-router-1
      host: 10.97.161.185
      name: edge
      port: "45671"
  tlsCredentials: south-ac619
---
apiVersion: v1
kind: Secret
type: kubernetes.io/tls
metadata:
  name: south-ac619
data:
  ca.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURKekNDQWcrZ0F3SUJB [...]
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURORENDQWh5Z0F3SUJ [...]
  tls.key: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0N [...]

# Generate a Link resource and direct the output to a file
$ skupper link generate > link.yaml
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

Endpoint Host



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-name">--name</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

Router Access Name ``` ``` -n, --namespace string   Set the namespace -p, --platform string    Set the platform type to use [kubernetes, podman, docker, linux] ```



</div>
</div>

## Global options
