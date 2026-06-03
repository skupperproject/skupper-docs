---
body_class: object command
refdog_links:
- title: Site configuration
  url: /docs/refdog/topics/site-configuration.html
- title: Site concept
  url: /docs/refdog/concepts/site.html
- title: Site resource
  url: /docs/refdog/resources/site.html
refdog_object_has_attributes: true
render_macros: false
---

# Site generate command

~~~ shell
skupper site generate [options]
~~~

A site is a place where components of your application are running.
Sites are linked to form application networks.
There can be only one site definition per namespace.
Generate a site resource to evaluate what will be created with the site create command

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Examples

~~~ console
# Generate a Site resource and print it to the console
$ skupper site generate west --enable-link-access
apiVersion: skupper.io/v2alpha1
kind: Site
metadata:
  name: west
spec:
  linkAccess: default

# Generate a Site resource and direct the output to a file
$ skupper site generate east > east.yaml
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-enable-link-access">--enable-link-access</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

allow access for incoming links from remote sites (default: false)

<table class="fields"><tr><th>Default</th><td><p><code>false</code></p>
</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for generate -o, --output string        print resources to the console instead of submitting them to the Skupper controller. Choices: json, yaml (default "yaml") ``` ``` -n, --namespace string   Set the namespace -p, --platform string    Set the platform type to use [kubernetes, podman, docker, linux] ```

<table class="fields"><tr><th>Default</th><td><p><code>&quot;yaml&quot;</code></p>
</td></table>

</div>
</div>

## Global options
