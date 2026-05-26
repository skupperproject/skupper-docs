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

# Link status command

~~~ shell
skupper link status [options]
~~~

Display the status of links in the current site.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Examples

~~~ console
# Show the status of all links in the current site
$ skupper link status
NAME          STATUS   COST
west-6bfn6    Ready    1
south-ac619   Error    10

Links from remote sites:

<none>

# Show the status of one link
$ skupper link status west-6bfn6
Name:     west-6bfn6
Status:   Ready
Message:  <none>
Cost:     1
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">boolean</div>
</div>
<div class="attribute-body">

help for status -o, --output string   print resources to the console instead of submitting them to the Skupper controller. Choices: json, yaml ``` ``` -n, --namespace string   Set the namespace -p, --platform string    Set the platform type to use [kubernetes, podman, docker, linux] ```



</div>
</div>

## Global options
