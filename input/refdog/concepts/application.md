---
body_class: object concept
refdog_links:
- title: Network concept
  url: /docs/refdog/concepts/network.html
- title: Component concept
  url: /docs/refdog/concepts/component.html
render_macros: false
---

# Application concept

An application is a set of [components](component.html) that work
together.  A Skupper [network](network.html) is dedicated to one
application.

<figure>
  <img src="images/application-model.svg" style="max-height: 5em;"/>
  <figcaption>The application model</figcaption>
</figure>

An application has one or more components.

<figure>
  <img src="images/application-1.svg"/>
  <figcaption>A simple application with two components</figcaption>
</figure>

<figure>
  <img src="images/application-2.svg"/ style="max-height: 30em; max-width: 90%;">
  <figcaption>The components of the Online Boutique example application</figcaption>
</figure>
