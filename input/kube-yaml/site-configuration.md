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

   If you need to link to this site, enable link access:
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: Site
   metadata:
     name: my-site
     namespace: west
   spec:
     linkAccess: default
   ```
   

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

By default, the router CPU allocation is BestEffort as described in [Pod Quality of Service Classes](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/) and this might affect performance under network load.
Consider setting resources as described in [Setting site resources](#kube-site-resources-yaml).

There are many options to consider when creating sites using YAML, see the [YAML Reference][yaml-ref], including *frequently used* options.

[yaml-ref]: https://skupperproject.github.io/refdog/resources/index.html


<a id="kube-site-resources-yaml"></a>
## Setting site resources

You can configure the Skupper Router and Kube Adaptor components with minimum and maximum CPU and memory resources by defining sizing models using ConfigMaps.

**Note:** Increasing the number of routers does not improve network performance. An incoming router-to-router link is associated with just one active router. Additional routers do not receive traffic while that router is responding.

**Prerequisites**

* The Skupper V2 controller is running in your cluster.
* You have determined the router CPU allocation you require.

  Consider the following CPU allocation options:

  | Router CPU | Description |
  |------------|-------------|
  | 1 | Helps avoid issues with BestEffort on low resource clusters |
  | 2 | Suitable for production environments |
  | 5 | Maximum performance |

Procedure

1. Create a sizing ConfigMap in the same namespace where your Skupper V2 controller is running.

   The following example defines a sizing configuration named `medium` with 2 CPU cores suitable for production:

   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: sizing-medium
     labels:
       skupper.io/site-sizing: "medium"
     annotations:
       skupper.io/default-site-sizing: "true"
   data:
     router-cpu-limit: "2"
     router-memory-limit: 1024Mi
   ```

   The Skupper controller selects ConfigMaps based on the presence of a `skupper.io/site-sizing` label.
   The label's value serves as an internal identifier for that particular sizing configuration.

   To designate a sizing model as the default for all sites managed by your Skupper V2 controller instance, annotate the ConfigMap with `skupper.io/default-site-sizing: "true"`.

   A sizing ConfigMap can define the following fields:

   - `router-cpu-request`
   - `router-cpu-limit`
   - `router-memory-request`
   - `router-memory-limit`
   - `adaptor-cpu-request`
   - `adaptor-cpu-limit`
   - `adaptor-memory-request`
   - `adaptor-memory-limit`

   **Note:** If only the `limit` field is defined, Kubernetes will also set the `request` with the same value. If this is not what you want, make sure to set the respective `request` field with a smaller value.

2. Determine the controller namespace.
   Depending on your installation method, the controller namespace may be `skupper` or have a different name.
   You can check that you have chosen the correct namespace by running:

   ```
   kubectl get pods
   ```

   Confirm that the skupper controller pod is running in the namespace.

3. Apply the ConfigMap in the controller namespace:

   ```bash
   kubectl apply -f sizing-medium.yaml
   ```

4. Assign the sizing configuration to a site by setting the `spec.settings.size` field in the site resource:

   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: Site
   metadata:
     name: my-site
   spec:
     settings:
       size: medium
   ```

5. Verify the resource limits have been applied by inspecting the `skupper-router` deployment:

   ```bash
   kubectl get deployment skupper-router -o json | jq .spec.template.spec.containers[].resources
   ```

   The output should look like:

   ```json
   {
     "limits": {
       "cpu": "1",
       "memory": "1Gi"
     },
     "requests": {
       "cpu": "500m",
       "memory": "512Mi"
     }
   }
   ```

You can define multiple sizing configurations using separate ConfigMaps.
Only one ConfigMap should be annotated as the default (`skupper.io/default-site-sizing: "true"`).
The default annotation is optional. If no default is specified, sites will use the `small` sizing configuration with BestEffort QoS.

