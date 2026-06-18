<a id="kube-cli"></a>
# Overview of Skupper CLI on Kubernetes
<!--REFERENCE-->

You can use the `skupper` CLI on Kubernetes after installing the Skupper controller to configure sites, links and services. 

The Skupper CLI is designed to generate and consume standard resources, ensuring that a sites, links and services configured using the CLI are identical to those configured directly through YAML.

* [Create sites][site-configuration]
* [Link sites][site-linking] (requires that one site has link access enabled)
* [Configure link cost][link-cost]
* [Expose and consume services][service-exposure]

[site-configuration]: ./site-configuration.html
[site-linking]: ./site-linking.html
[link-cost]: ./site-linking.html#kube-link-cost-cli
[service-exposure]: ./service-exposure.html
