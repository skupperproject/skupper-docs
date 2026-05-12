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

# Site create command

~~~ shell
skupper site create [options]
~~~

A site is a place where components of your application are running.
Sites are linked to form application networks.
There can be only one site definition per namespace.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td><tr><th>Waits for</th><td>Ready</td></table>

## Examples

~~~ console
# Create a site
$ skupper site create west
Waiting for status...
Site "west" is ready.

# Create a site that can accept links from remote sites
$ skupper site create west --enable-link-access
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-enable-ha">--enable-ha</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

Configure the site for high availability (EnableHA). EnableHA sites have two active routers



</div>
</div>

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

help for create



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-link-access-type">--link-access-type</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

configure external access for links from remote sites. Choices: [route|loadbalancer]. Default: On OpenShift, route is the default; for other Kubernetes flavors, loadbalancer is the default.

<table class="fields"><tr><th>Choices</th><td><table class="choices"><tr><th><code>route</code></th><td></td></tr><tr><th><code>loadbalancer</code></th><td></td></tr></table></td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-timeout">--timeout</h3>
<div class="attribute-type-info">&lt;duration&gt;</div>
</div>
<div class="attribute-body">

raise an error if the operation does not complete in the given period of time (expressed in seconds). (default 3m0s)

<table class="fields"><tr><th>Default</th><td><p><code>3m0s</code></p>
</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-wait">--wait</h3>
<div class="attribute-type-info">&lt;string&gt;</div>
</div>
<div class="attribute-body">

Wait for the given status before exiting. Choices: configured, ready, none (default "ready") ``` ``` -c, --context string      Set the kubeconfig context

<table class="fields"><tr><th>Default</th><td><p><code>&quot;ready&quot;</code></p>
</td></table>

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

## Errors

- **A site resource already exists**

  <p>There is already a site resource defined for the namespace.</p>
