---
body_class: object command
refdog_links: []
refdog_object_has_attributes: true
render_macros: false
---

# Debug cert-inspect command

~~~ shell
skupper debug cert-inspect [options]
~~~

Decode and display key fields of X.509 certificates managed by Skupper,
including subject, issuer, validity period, SANs, and public key information.
Without a name, all certificates in the namespace are listed. With a name,
detailed information for that certificate is shown.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Examples

~~~ console
# List all certificates
$ skupper debug cert-inspect

# Inspect a named certificate
$ skupper debug cert-inspect skupper-local-server

# Inspect a local PEM file
$ skupper debug cert-inspect --file /path/to/tls.crt
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-file">--file</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

Inspect a local PEM-encoded certificate file



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for cert-inspect -o, --output string   print resources to the console instead of submitting them to the Skupper controller. Choices: json, yaml ``` ``` -n, --namespace string   Set the namespace -p, --platform string    Set the platform type to use [kubernetes, podman, docker, linux] ```



</div>
</div>

## Global options
