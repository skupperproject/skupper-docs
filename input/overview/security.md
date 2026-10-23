<a id="skupper-security"></a>
# Security
<!--CONCEPT-->

{{skupper_name}} protects service-to-service communication with built-in mutual TLS security.

{{skupper_name}} securely connects your services with TLS authentication and encryption.
See how {{skupper_name}} enables you to deploy your application securely across Kubernetes clusters.

**Security challenges in the cloud**

Moving an application to the cloud raises security risks.
Either your services must be exposed to the public internet, or you must adopt complex layer 3 network controls like VPNs, firewall rules, and access policies.

Increasing the challenge, layer 3 network controls do not extend easily to multiple clusters.
These network controls must be duplicated for each cluster.

**Built-in network isolation**

{{skupper_name}} provides default, built-in security that scales across clusters and clouds.
In a {{skupper_name}} network, the connections between {{skupper_name}} routers are secured with mutual TLS using a private, dedicated certificate authority (CA).
Each router is uniquely identified by its own certificate.

![Three clusters connected by {{skupper_name}} routers with mutual TLS links between each router](../images/clusters-tls.svg)

This means that the {{skupper_name}} network is isolated from external access, preventing security risks such as lateral attacks, malware infestations, and data exfiltration.
