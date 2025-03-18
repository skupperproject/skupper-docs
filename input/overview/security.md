<a id="skupper-security"></a>
# Skupper security

Skupper securely connects your services with TLS authentication and encryption.
See how Skupper enables you to deploy your application securely across Kubernetes clusters.

**Security challenges in the cloud**

Moving an application to the cloud raises security risks.
Either your services must be exposed to the public internet, or you must adopt complex layer 3 network controls like VPNs, firewall rules, and access policies.

Increasing the challenge, layer 3 network controls do not extend easily to multiple clusters.
These network controls must be duplicated for each cluster.

**Built-in network isolation**

Skupper provides default, built-in security that scales across clusters and clouds.
In a Skupper network, the connections between Skupper routers are secured with mutual TLS using a private, dedicated certificate authority (CA).
Each router is uniquely identified by its own certificate.

![clusters-tls](../images/clusters-tls.svg)

This means that the Skupper network is isolated from external access, preventing security risks such as lateral attacks, malware infestations, and data exfiltration.

