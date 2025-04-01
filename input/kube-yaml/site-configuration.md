<a id="kube-creating-site-yaml"></a>
# Creating a site on Kubernetes using YAML

Using YAML allows you to create and manage sites from the context of the current namespace.

A typical workflow is to create a site, link sites together, and expose services to the application network.

<a id="kube-creating-simple-site-yaml"></a>
## Creating a simple site on Kubernetes using YAML

You can use YAML to create and manage Skupper sites.

**Prerequisites**

* The Skupper controller is running on the Kubernetes cluster you are running or you are running on a platform.

Procedure

1. Create a site CR YAML file named `my-site.yaml`, for example:

   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: Site
   metadata:
     name: my-site
     namespace: west
   ```
   This YAML creates a site named `my-site` in the `west` namespace.
   Specifying the namespace is not required if the context is set to the namespace where you want to create the site.

2. Create the site:
   ```bash
   kubectl apply -f my-site.yaml
   ```

3. Check the status of the site:
   ```bash
   kubectl get site
   ```
   You might need to issue the command multiple times before the site is ready:
   ```
   $ kubectl get site
   NAME   STATUS    SITES IN NETWORK   MESSAGE
   west   Pending                      containers with unready status: [router kube-adaptor]
   $ kubectl get site
   NAME   STATUS   SITES IN NETWORK   MESSAGE
   west   Ready    1                  OK
   ```
   You can now link this site to another site to create an application network.

There are many options to consider when creating sites using YAML, see [YAML Reference][yaml-ref], including *frequently used* options.

[yaml-ref]: https://skupperproject.github.io/refdog/resources/index.html