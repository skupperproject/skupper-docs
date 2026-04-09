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

**Certificates and trust between sites**

On Kubernetes, each site has its own certificate authority for inter-site communication.
By default, Skupper generates the certificates needed to identify the router and to authenticate incoming and outgoing links.

When two sites are linked, each router verifies the certificate presented by the remote router and checks that it is signed by a trusted CA.
This mutual TLS exchange ensures that only sites with valid credentials can join the application network.

If your environment requires certificates issued by your own PKI, you can replace the default server certificate that a site uses for incoming links and provide matching client credentials for connecting sites.
This allows you to keep Skupper's mutual TLS model while aligning certificate management with your organization's security requirements.

**Service level TLS**

Skupper always encrypts traffic between sites.
This protects traffic carried across the application network, even when workloads run in different clusters or clouds.

This inter-site encryption is separate from any TLS configuration used by your application services.
If a backend service also requires TLS, you can configure listener and connector resources with appropriate credentials for the application side of the connection.
