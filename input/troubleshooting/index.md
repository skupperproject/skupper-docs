<a id="troubleshooting"></a>
# Troubleshooting an application network
<!--ASSEMBLY-->

Typically, you can create a network without referencing this troubleshooting guide.
However, this guide provides some tips for situations when the network does not perform as expected.

A typical troubleshooting workflow is to check all the sites and create debug tar files.

<a id="checking-sites"></a>
## Checking sites
<!--PROCEDURE-->

Check site, connector, listener, and link status to confirm that the application network is operating correctly.

Using the `skupper` command-line interface (CLI) provides a simple method to get started with troubleshooting Skupper.

**Procedure**

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
<!--PROCEDURE-->

Check link status to confirm that sites can exchange traffic across the application network.

You must link sites before you can expose services on the network.

**📌 NOTE**
By default, tokens expire after 15 minutes and you can only use a token once.
Generate a new token if the link is not connected.

This section outlines some advanced options for checking links.

**Procedure**

1. Check the link status:

   ```bash
   skupper link status -n east
   
   NAME                                            STATUS  COST    MESSAGE
   west-48b5feee-89e9-4a53-b8d0-e94304cc951f       Ready   1       OK
   ```

   A link exists from the specified site to another site, meaning a token from another site was applied to the specified site.

   The status of the link must be `Ready` to allow service traffic.

   **📌 NOTE**
   You must run `skupper link status` on a linking site.

   If you use this command on a connecting site, there is a message:

   ```
   skupper link status -n west

   There are no link resources in the namespace
   ```


<a id="checking-kube-router"></a>
## Checking the router on Kubernetes sites
<!--PROCEDURE-->

Monitor router pod health and detect when the router becomes unavailable.

The Skupper controller monitors router pods. When no router pod is running and ready, the Site CR status is updated to reflect the router's unavailability.

**Procedure**

1. Check router pod readiness directly:

   ```bash
   kubectl get pods -l skupper.io/component=router
   ```

   A healthy site shows `2/2` ready (both `router` and `kube-adaptor` containers). A problem looks like:

   ```
   NAME                             READY   STATUS    RESTARTS   AGE  
   skupper-router-6d9f7b8c4-xk2p9   1/2     Running   0          3m
   ```

   To see which container is not ready and why:

   ```bash
   kubectl describe pod -l skupper.io/component=router
   ```

   Look at the `Conditions` and `Events` sections.

2. Check kube-adaptor logs for AMQP connectivity issues:

   The `kube-adaptor` sidecar runs inside the router pod (not `skupper-controller`). It logs errors when it cannot reach the router over AMQP:

   ```bash
   kubectl logs -l skupper.io/component=router -c kube-adaptor
   ```

   Look for:

   ```
   component=kube.adaptor.configSync  level=ERROR  msg="sync failed"  error="Could not get management agent : ..."
   ```

3. Observe router pod restarts:

   ```bash
   kubectl get events -n <namespace> --field-selector reason=Killing
   kubectl rollout status deploy/skupper-router
   ```

   When the router pod restarts and becomes ready, the controller sets `Running=True` and `Ready=True`. The `kube-adaptor` reconnects and re-syncs the bridge configuration.

   **📌 NOTE**
   All existing TCP connections through the router are lost when the router pod is terminated. Clients will see `connection reset` or `EOF`. After the router restarts, new connections can be established, but existing connections are not restored.


<a id="checking-nonkube-router"></a>
## Checking the router on local system sites
<!--PROCEDURE-->

Monitor router process health on local system sites using heartbeat logs and site status.

On local system sites, the Skupper controller monitors the router using AMQP heartbeats. The `heartbeat.client` component logs state changes when the router becomes unavailable or recovers.

**Procedure**

1. Monitor controller logs for router heartbeat status:

   ```bash
   podman logs <username>-skupper-controller -f
   # or
   docker logs <username>-skupper-controller -f
   ```

   Look for:

   ```
   component=heartbeat.client  Router is DOWN  reason=<reason>
   component=heartbeat.client  Router is UP
   ```

   `Router is DOWN` is logged when the heartbeat connection to the router is lost (for example, the router process exits or is killed). `Router is UP` is logged when the heartbeat connection is re-established.

2. Check site status:

   ```bash
   skupper site status
   ```

   This shows whether the router process is running and healthy.

3. Understand service behavior during router downtime:

   The controller stops all dependent services when the router goes down and restarts them when the router comes back up.

   **📌 NOTE**
   All existing TCP connections through the router are lost when the router process exits. Clients will see `connection reset` or `EOF`. After the router restarts and the controller logs `Router is UP`, new connections can be established.


<a id="tcp-client-errors"></a>
## Understanding TCP client errors when backends fail
<!--REFERENCE-->

  
When backend pods are removed or crash, Skupper removes the corresponding  routing entries from the router. 
Existing TCP connections that were routed  through those backends are terminated. 
The error seen by the TCP client  depends on how the pod was removed:  
  
| Scenario | Client-visible error |  
| --- | --- |  
| Graceful pod termination (SIGTERM, scale-down) | `EOF` or `connection reset` — the pod closes its socket before the router removes the backend |  
| Pod crash or OOM kill | `connection reset` — the kernel sends a TCP RST |  
| Router removes the backend before pod terminates | `connection reset` or `EOF` depending on timing |  
  
There is no grace period or connection draining at the Skupper router level when a backend is removed. 
Clients must implement reconnect logic to recover from these errors.  
  
New connections attempted after the backend is removed will receive  `connection refused` if no backend pods are available, because the router has no target to forward to.


<a id="dynamic-system-controller"></a>
## Troubleshooting the Dynamic System Controller
<!--PROCEDURE-->

The Dynamic System Controller feature (available on Docker and Podman platforms only) enables automatic processing of YAML resources when `--reload-type=auto` is enabled during installation. 

Use this section to diagnose issues when resources are not being automatically detected or processed.

By default, the reload type is set to `manual`, meaning resources must be processed by using `skupper system start` and `skupper system reload` for subsequent changes.

**Procedure**

1. Verify the controller is configured for auto-reload:

   Check the system controller container logs:
   ```bash
   podman logs <username>-skupper-controller
   # or
   docker logs <username>-skupper-controller
   ```

   Look for the configuration line:
   ```
   INFO System Reload: type=auto
   ```

2. Monitor resource detection:

   When the controller detects a new resource file, it logs:
   ```
   Resource has been created: backend.yaml
   ```

   If you don't see this message after copying a YAML file to the `/input/resources` directory, check:
   - The file is in the correct directory for the namespace
   - The file has valid YAML syntax
   - The file has correct permissions

3. Verify resource processing:

   Check that files copied to the `/input/resources` directory appear in the `/runtime/resources` directory after processing.

   Check the status of resources using the CLI:
   ```bash
   skupper connector status
   skupper listener status
   skupper link status
   ```

4. Review controller logs for errors:

   Look for processing errors or validation failures:
   ```bash
   podman logs <username>-skupper-controller | grep -i error
   # or
   docker logs <username>-skupper-controller | grep -i error
   ```


<a id="setting-log-levels"></a>
## Setting controller log levels
<!--PROCEDURE-->

Change the Skupper controller log level dynamically without restarting the controller.

The controller watches a ConfigMap named `skupper-log-config` in its namespace for live log level changes. You just need to create (or update) that ConfigMap with the key `CONTROLLER_LOG_LEVEL`.

**Procedure**

1. Enable debug logging:

   If the ConfigMap does not exist, create it:

   ```bash
   kubectl create configmap skupper-log-config \
     --from-literal=CONTROLLER_LOG_LEVEL=debug \
     -n <your-namespace>
   ```

   If the ConfigMap already exists:

   ```bash
   kubectl patch configmap skupper-log-config \
     -n <your-namespace> \
     --type merge \
     -p '{"data":{"CONTROLLER_LOG_LEVEL":"debug"}}'
   ```

   The change is picked up dynamically — no restart needed.

2. Set the desired log level:

   Valid values are:
   - `debug` - Most verbose, shows all operations
   - `info` - Default level, shows normal operations
   - `warn` - Shows warnings and errors only
   - `error` - Shows errors only

3. Revert to default logging:

   Delete the ConfigMap to revert to `info` level:

   ```bash
   kubectl delete configmap skupper-log-config -n <your-namespace>
   ```


<a id="debug-dump"></a>
## Creating a Skupper debug tar file
<!--PROCEDURE-->

Create a debug tar file containing diagnostic information about a Skupper site to troubleshoot issues or share with support.

The `skupper debug dump` command creates a compressed tarball (`.tar.gz`) containing logs, configurations, and resource status from a site. The output file is named using the pattern `<filename>-<namespace>-<datetime>.tar.gz`. If no filename is provided, it defaults to `skupper-dump`.

This procedure applies to both Kubernetes and local system sites.

**Procedure**

1. Create the debug tar file for a site:

   ```bash
   skupper debug dump
   ```

   Or specify a custom filename:

   ```bash
   skupper debug dump mysite-debug
   ```

   The command creates a file such as `skupper-dump-default-20250526-143022.tar.gz`.

2. Extract the tar file to examine its contents:

   ```bash
   mkdir skupper-dump
   tar -xzf skupper-dump-default-20250526-143022.tar.gz -C skupper-dump
   cd skupper-dump
   ```

3. Check the Skupper and platform versions:

   - `/versions/kubernetes.yaml` - Kubernetes version (on Kubernetes platforms)
   - `/versions/skupper.yaml` - Versions of Skupper components

4. Check the site configuration and ingress:

   - `/site-namespace/resources/Site-<name>.yaml` - Site specification and status
   - `/site-namespace/resources/RouterAccess-<name>.yaml` - Ingress and access type configured for the site

5. Check linking and service configuration:

   - `/site-namespace/resources/Link-<name>.yaml` - Link status between sites
   - `/site-namespace/resources/Accessgrant-<name>.yaml` - Access grants for tokens
   - `/site-namespace/resources/AccessTokens-<name>.yaml` - Token usage information
   - `/site-namespace/resources/Connector-<name>.yaml` - Connector configuration and status
   - `/site-namespace/resources/Listener-<name>.yaml` - Listener configuration and status


You may notice resources that contain labels prefixed with `internal.skupper.io/`.

**📌 NOTE**
Labels prefixed with `internal.skupper.io/` are **internal-only**. They are subject to change without notice in future versions of Skupper. Do not modify, delete, or build automation that depends on the state or existence of these labels.

