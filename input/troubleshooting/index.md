<a id="troubleshooting"></a>
# Troubleshooting an application network
<!--ASSEMBLY-->

Typically, you can create a network without referencing this troubleshooting guide.
However, this guide provides some tips for situations when the network does not perform as expected.

See the resolving common problems section if you have encountered a specific issue using the `skupper` CLI.

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

4. Check the status of any links:

   ```bash
   skupper link status

   ```

   The output shows the links .

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
   Running `skupper link status` on a linked site produces output only if a token was used to create a link.

   If you use this command on a site where you did not create the link, but there is an incoming link to the site:

   ```
   skupper link status -n west

   There are no link resources in the namespace
   ```

<a id="resolving-common-problems"></a>
## Resolving common problems
<!--REFERENCE-->

Use these common symptoms and messages to identify simple Skupper configuration problems.

The following issues and workarounds might help you debug simple scenarios when evaluating Skupper.

- Container platform error:

  ```
  Failed to bootstrap: failed to load site state: error loading "/home/user/.local/share/skupper/namespaces/default/input/resources/sites/test.yaml": multiple sites found, but only one site is allowed for bootstrapping
  ```

- namespace error:
  ```
  there is already a site created for this namespace
  ```

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
