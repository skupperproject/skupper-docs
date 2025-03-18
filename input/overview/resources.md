<a id="kube-resources"></a>
# Skupper resources on Kubernetes

The following sections describe the various Skupper resources on Kubernetes, for example, service accounts

<a id="kube-resources-crds"></a>
## Custom resource definitions

To get start creating application networks, you create the following custom resources:

* Sites
* Links
* Connectors
* Listeners

See [Resource Reference][yaml-ref] for explanations of all the custom resources.

<a id="kube-resources-sa"></a>
## Service accounts, roles and role bindings

When you install the Skupper controller, the following resources are created:

* **skupper-controller**
A service account, role and role binding with this name are created to manage the Skupper  controller.


When you create a Skupper site, the following resources are created:

* **skupper-router**
A service account, role and role binding with this name are created to manage the Skupper router.

<a id="kube-resources-deployments"></a>
## Deployments

The Skupper controller deploys the **skupper-controller**, which provides the control plane for the application network.

Each Skupper site on Kubernetes deploys a **skupper-router**, which provides the data plane for the application network.

<a id="kube-resources-cm"></a>
## ConfigMaps

Do not edit these ConfigMap values directly.

* **skupper-site**
site settings, including:

  * console authentication
  * ingress strategy

  This ConfigMap is the root object for all the skupper resources; deleting it will remove the Skupper deployment from the namespace.
* **skupper-services**
internal representation of the services available on the application network.
* **skupper-internal**
internal router configuration.
The service controller determines the values in this ConfigMap based on the services available on the application network.

<a id="kube-resources-secrets"></a>
## Secrets

Each site has two `kubernetes.io/tls` type secrets, **skupper-local-ca** and **skupper-site-ca**:

* **skupper-local-ca**
issues certs for local access. 

  The local certs are held in:  
  * **skupper-local-server** used by the router.

* **skupper-site-ca**
issues certs for remote access.

  The site ca issued certs are **skupper-site-server** which holds the certs that identify the router to other routers that link to this site.

The tokens used to establish links creates the following secrets with variable names:
+
* The site that issues a token generates a secret with a UUID name that contains details of any usage restrictions, for example, the number of times you can use the token to create a link and the amount of time the token is valid for.
* The site establishing the link will have a secret that contains the token. 
These secrets are typically called `link-<remote-site-name>`. 

<a id="kube-resources-svc"></a>
## Services

In addition to the services that are exposed on the application network, the following services are created:

* **skupper-router-local**
The service controller uses this service to connect to and configure the router. 
* **skupper-router**
Other sites use this service to access the router over the inter-router or edge ports, although there may be other resources involved, for example, an ingress. 


[yaml-ref]: https://skupperproject.github.io/refdog/resources/index.html