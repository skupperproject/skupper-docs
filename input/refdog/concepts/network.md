---
body_class: object concept
refdog_links:
- title: Site linking
  url: /docs/refdog/topics/site-linking.html
- title: Site concept
  url: /docs/refdog/concepts/site.html
- title: Link concept
  url: /docs/refdog/concepts/link.html
render_macros: false
---

# Network concept

A network is a set of [sites](site.html) joined by
[links](link.html). A Skupper network is also known as an
application network or virtual application network (VAN).

<figure>
  <img src="images/network-model.svg" style="max-height: 5em;"/>
  <figcaption>The network model</figcaption>
</figure>

A network has one or more sites.  Each site belongs to only one
network.

Each site in the network can expose services to other sites in the
network. In turn, each site in the network can access those exposed
services.  Each network is meant for one distributed application.
This provides isolation from other applications and networks.

<figure>
  <img src="images/network-1.svg"/>
  <figcaption>A simple network with two sites</figcaption>
</figure>

<figure>
  <img src="images/network-2.svg"/>
  <figcaption>A larger network</figcaption>
</figure>
