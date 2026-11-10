# Skupper documentation

This documentation is organized around the main ways people learn and use Skupper: 
- understanding the model
- getting started with the CLI
- creating networks declaratively
- exploring the concepts in depth
- looking up reference material

## Get started with the CLI

Use the CLI when you want the fastest path to creating a site, linking sites together, and exposing services.
The installation guide covers the controller and CLI setup, and the task-oriented CLI guides show how to build an application network on Kubernetes or local systems.

- [Getting started](https://skupper.io/start/index.html)

## Create application networks declaratively

Use the declarative YAML workflow when you want infrastructure that is defined in version-controlled manifests.
These guides show how to describe sites, links, and service exposure for Kubernetes and local-system deployments.

* [Kubernetes YAML overview](kube-yaml/index.html)
* [Configure sites with Kubernetes YAML](kube-yaml/site-configuration.html)
* [Link sites with Kubernetes YAML](kube-yaml/site-linking.html)
* [Expose services with Kubernetes YAML](kube-yaml/service-exposure.html)
* [System YAML overview](system-yaml/index.html)
* [Configure sites with system YAML](system-yaml/site-configuration.html)
* [Link sites with system YAML](system-yaml/site-linking.html)
* [Expose services with system YAML](system-yaml/service-exposure.html)

## Kubernetes

* [Kubernetes CLI overview](kube-cli/index.html)
* [Create sites using the CLI](kube-cli/site-configuration.html)
* [Link sites using the CLI](kube-cli/site-linking.html)
* [Expose services using the CLI](kube-cli/service-exposure.html)
* [Kubernetes YAML overview](kube-yaml/index.html)
* [Create sites using YAML](kube-yaml/site-configuration.html)
* [Link sites using YAML](kube-yaml/site-linking.html)
* [Expose services using YAML](kube-yaml/service-exposure.html)
* [Custom certificates](kube-yaml/custom-certs.html)

## Local systems

* [Local systems CLI overview](system-cli/index.html)
* [Create sites using the CLI](system-cli/site-configuration.html)
* [Link sites using the CLI](system-cli/site-linking.html)
* [Expose services using the CLI](system-cli/service-exposure.html)
* [Local systems YAML overview](system-yaml/index.html)
* [Create sites using YAML](system-yaml/site-configuration.html)
* [Link sites using YAML](system-yaml/site-linking.html)
* [Expose services using YAML](system-yaml/service-exposure.html)

## Explore conceptual deep dives

The Reference section provides a more detailed look at the Skupper model, terminology, and operational topics.
Use it when you want to understand the platform beyond the getting-started flows.

* [Reference home](refdog/index.html)
* [Skupper concepts](refdog/concepts/index.html)
* [Operational topics](refdog/topics/index.html)

## Reference material

When you need exact command or resource definitions, go straight to the reference sections.

* [CLI reference](refdog/commands/index.html)
* [Resource reference](refdog/resources/index.html)
* [Console guide](console/index.html)
* [Troubleshooting](troubleshooting/index.html)
