<a id="skupper-routing"></a>
# Skupper routing

Skupper uses layer 7 addressing and routing to connect services.
See how the power of application-layer addressing can bring new capabilities to your applications.

**Multi-cluster services**

Deploy a single logical service across multiple clusters.

Skupper can route requests to instances of a single service running on multiple clusters.
If a provider or data center fails, the service instances running at unaffected sites can scale to meet the need and maintain availability.

**Dynamic load balancing**

Balance requests across clusters according to service capacity.

The Skupper network has cross-cluster visibility.
It can see which services are already loaded and which have spare capacity, and it directs requests accordingly.

You can assign a cost to each inter-cluster connection.
This enables you to configure a preference for one resource over another.
If demand is normal, you can keep all traffic on your private cloud.
If demand peaks, you can dynamically spill over to public cloud resources.

**Reliable networks**

Skupper uses redundant network paths and smart routing to provide highly available connectivity at scale.
