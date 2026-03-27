<a id="troubleshooting"></a>
# Troubleshooting an application network

Typically, you can create a network without referencing this troubleshooting guide.
However, this guide provides some tips for situations when the network does not perform as expected.

See [Resolving common problems](#resolving-common-problems) if you have encountered a specific issue using the `skupper` CLI.

A typical troubleshooting workflow is to check all the sites and create debug tar files.

<a id="checking-sites"></a>
## Checking sites

Using the `skupper` command-line interface (CLI) provides a simple method to get started with troubleshooting Skupper.

1. Check the controller on Kubernetes.
   On Kubernetes the controller must be installed before you attempt to create an application network.
2. Check the site status for a cluster:

   ```bash
   skupper site status

   NAME    STATUS  MESSAGE
   west    Ready   OK
   ```

   The output shows:

   - Sites exist in the specified namespace on Kubernetes.
   - On other platforms, the status shows all sites for the user.

   On Kubernetes, you can also check the resource, for example:

   ```bash
   kubectl get site -o yaml
   
   apiVersion: v1
   items:
   - apiVersion: skupper.io/v2alpha1
     kind: Site
     metadata:
       annotations:
         kubectl.kubernetes.io/last-applied-configuration: |
           {"apiVersion":"skupper.io/v2alpha1","kind":"Site","metadata":{"annotations":{},"name":"west","namespace":"default"}}
       creationTimestamp: "2025-02-24T09:33:51Z"
       generation: 1
       name: west
       namespace: default
       resourceVersion: "701"
       uid: d6bc9342-6f7e-4f9a-a643-053a6a0e2335
     status:
       conditions:
       - lastTransitionTime: "2025-02-24T09:33:51Z"
         message: OK
         observedGeneration: 1
         reason: Ready
         status: "True"
         type: Configured
       - lastTransitionTime: "2025-02-24T09:34:21Z"
         message: OK
         observedGeneration: 1
         reason: Ready
         status: "True"
         type: Ready
       - lastTransitionTime: "2025-02-24T09:34:21Z"
         message: OK
         observedGeneration: 1
         reason: Ready
         status: "True"
         type: Running
       controller:
         name: skupper-controller
         namespace: default
         version: 2.1.1-rc1
       defaultIssuer: skupper-site-ca
       message: OK
       network:
       - id: d6bc9342-6f7e-4f9a-a643-053a6a0e2335
         name: west
         namespace: default
         platform: kubernetes
         version: 2.1.1-rc1
       sitesInNetwork: 1
       status: Ready
   kind: List
   metadata:
     resourceVersion: ""
   ```

   If this command fails, check the controller.

3. Check connectors and listeners:

   ```bash
   skupper connector status
   
   NAME    STATUS  ROUTING-KEY     SELECTOR        HOST    PORT    HAS MATCHING LISTENERMESSAGE
   backend Ready   backend         app=backend             8080    true                 OK
   ```

   The output shows:

   - There is one connector, named `backend`.
   - The connector uses the `backend` routing key and port `9090`.

   This result shows that you can create a listener using the `backend` routing key and port `9090` on a different site to access the `backend` service.


<a id="checking-links"></a>
## Checking links

You must link sites before you can expose services on the network.

**📌 NOTE**
By default, tokens expire after 15 minutes and you can only use a token once.
Generate a new token if the link is not connected.

This section outlines some advanced options for checking links.

1. Check the link status:

   ```bash
   skupper link status -n east
   
   NAME                                            STATUS  COST    MESSAGE
   west-48b5feee-89e9-4a53-b8d0-e94304cc951f       Ready   1       OK
   ```

   A link exists from the specified site to another site, meaning a token from another site was applied to the specified site.

   The status of the link must be `Ready` to allow service traffic.

   **📌 NOTE**\
   You must run `skupper link status` on a linking site.

   If you use this command on a listening site, there is a message:

   ```
   skupper link status -n west

   There are no link resources in the namespace
   ```


<a id="checking-services"></a>
## Checking services

In a virtual application network (VAN), a service represents a logical endpoint that allows workloads in different sites to communicate over the application network without exposing those workloads directly to the underlying network.
Services are defined using listeners and connectors, which together describe where traffic enters the network and where it is delivered.

A listener defines how a service is exposed on a site.
It creates an address on the virtual network and accepts incoming TCP connections.
When a workload connects to the listener, the traffic is forwarded across the application network using the Skupper router in the listener site.

A connector defines where the service traffic is sent.
It associates the service with one or more backend workloads on Kubernetes or Linux, receiving the forwarded connections from the Skupper router in the connector site.
Multiple connectors can exist for the same service, allowing load distribution across sites.

Together, listeners and connectors allow a service to be reachable from any site in the application network while keeping the actual workloads local to their clusters.

This section explains the normal lifecycle of a connector, and how to observe what happens when backend pods are added or removed.

1. To observe the connector lifecycle, deploy a backend service and create a connector:

   ```bash
   kubectl create deployment backend --image=nginx
   kubectl expose deployment backend --port 8080
   ```

   ```bash
   skupper connector create backend 8080
   ```

2. Check the connector status:

   ```bash
   kubectl get connector
   ```

   ```bash
   kubectl get connector backend -o yaml
   ```

   The connector can be in one of the following states:

   * `Configured=False` - No backend pods are available
   * `Configured=True` - Backend pods are available and connected

   `Configured=False` reasons:   * No matches for selector - The selector does not match any pods

3. When you scale up the backend deployment, the connector detects the new pods and establishes connections:

   ```bash
   kubectl scale deployment backend --replicas 1
   ```

   Watch the controller logs to observe the connector lifecycle:

   ```bash
   kubectl logs deploy/skupper-controller -f
   ```

   You should see the following events:

   * Pod selected for connector
   * Router config updated
   * CREATE tcpConnector

4. When you scale down the backend deployment, the connector removes the connections:

   ```bash
   kubectl scale deployment backend --replicas 0
   ```

   You should see the following events:

   * DELETE tcpConnector
   * No pods available for connector
   * `Configured=False` status

5. Monitor the router logs to see when connectors are created or deleted:

   ```bash
   kubectl logs deploy/skupper-router -f
   ```

   You should see events such as:

   * CREATE tcpConnector
   * DELETE tcpConnector

6. When backend pods are unavailable, clients may encounter connection errors, for example:

   Remove the backend pods:

   ```bash
   kubectl scale deployment backend --replicas 0
   ```

   Possible connection errors include:

   * Connection reset
   * EOF (End of File)
   * Connection refused

7. When the router restarts, existing connections are lost and must be re-established:

   ```bash
   kubectl rollout restart deploy/skupper-router
   ```

   During the restart, connections are lost. The router logs may show:

   * Router is DOWN
   * Router is UP

8. When you delete a connector, the pod watcher stops and all connections are removed:

   ```bash
   skupper connector delete backend
   ```

   You should see the following events:

   * Stopping pod watcher
   * DELETE tcpConnector

9. The following table summarizes messages and logs in the connector lifecycle:

   Summary Table
   
   | Scenario | `kubectl logs` Component | Log Level | Log Message | CR Condition |
   | --- | --- | --- | --- | --- |
   | Connector pods → 0 (standard) | `kube.site.bindings` | DEBUG | `"No pods available for target selection"` | Connector: `Configured=False`, `message="No matches for selector"` |
   | Connector pods → 0 (attached) | `kube.site.attached_connector` | INFO | `"No pods available for selector"` | AttachedConnector + Binding: `Configured=False`, `message="No matches for selector"` |
   | No site for connector | `kube.site.site` | — (status only) | — | Connector: `Configured=False`, `message="No active site in namespace"` |
   | Router pod removed | — | — (no log) | *(silent)* | Site: `Running=False`, `Ready=False`, `message="No router pod is ready"` |
   | kube-adaptor: no AMQP | `kube.adaptor.configSync` | ERROR | `"sync failed"` + `"Could not get management agent"` | *(none — no CR updated)* |
   | kube-adaptor: bridge sync fail | `kube.adaptor.configSync` | ERROR | `"sync failed"` + `"Error while syncing bridge config"` | *(none)* |
   | kube-adaptor: init failure | `kube.adaptor.configSync` | ERROR | `"Error initialising config"` → exit(1) | *(none)* |
