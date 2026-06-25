<a id="kube-custom-labels"></a>
# Propagating custom labels and annotations using YAML
<!--ASSEMBLY-->

Skupper allows you to propagate custom labels and annotations onto the Kubernetes resources it manages by creating a specially-marked ConfigMap called a *label template*.

A label template is a standard Kubernetes ConfigMap that carries the label `skupper.io/label-template: "true"`. 
When the Skupper controller detects such a ConfigMap, it copies the ConfigMap's own labels and annotations onto the Skupper-managed resources in the same namespace (and optionally across all watched namespaces).

You may notice resources that contain labels prefixed with `internal.skupper.io/`.

**📌 NOTE**
Labels prefixed with `internal.skupper.io/` are generally reserved for system operations and subject to change without notice in future versions of Skupper. Do not modify, delete, or build automation that depends on the state or existence of these labels.
There is one exception to this advice, the `internal.skupper.io/listener` label is explicitly supported for use within label templates to allow you to target specific listener services. 


The controller watches these ConfigMaps dynamically: adding, updating, or deleting a label template takes effect on existing Skupper resources without restarting anything.



<a id="kube-creating-label-template"></a>
## Creating a label template using YAML
<!--PROCEDURE-->

Use a label template ConfigMap to propagate custom labels and annotations to all Skupper-managed resources.

**Prerequisites**

* The Skupper controller is running on the Kubernetes cluster.
* A Skupper site exists in the namespace where you want to apply labels.

**Procedure**

1. Create a label template YAML file named `my-labels.yaml`:

   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: my-label-template
     labels:
       skupper.io/label-template: "true"   # required marker
       acme.com/team: platform             # label to propagate
       environment: production             # label to propagate
     annotations:
       monitoring.acme.com/scrape: "true"  # annotation to propagate
   data: {}
   ```

   This ConfigMap propagates the `acme.com/team` and `environment` labels, plus the `monitoring.acme.com/scrape` annotation, to all Skupper-managed resources in the namespace.

2. Apply the label template:

   ```bash
   kubectl apply -f my-labels.yaml
   ```

   The labels and annotations are immediately applied to existing Skupper resources (Deployments, Services, ConfigMaps, Secrets, SecuredAccess resources) in the namespace.

3. Verify the labels were applied:

   ```bash
   kubectl get deployment skupper-router -o yaml | grep -A5 labels
   ```

   You should see your custom labels alongside the Skupper-managed labels.

**📌 NOTE**
The following labels and annotations are always excluded from propagation:

* `skupper.io/label-template`
* `kubectl.kubernetes.io/last-applied-configuration`

<a id="kube-label-template-scope"></a>
## Controlling label template scope
<!--PROCEDURE-->

Label templates can apply to a single namespace or to all namespaces managed by the Skupper controller.

**Namespace-scoped (applies to one site)**

Create the ConfigMap in the same namespace as the Skupper site.
Labels and annotations are applied only to resources in that namespace.

**Controller-scoped (applies to all sites)**

Create the ConfigMap in the Skupper controller's namespace.
Labels and annotations are applied to Skupper resources in every namespace the controller manages.

**📌 NOTE**
When both a namespace-scoped and a controller-scoped template define the same key, the controller-scoped value overrides the namespace-scoped one.

<a id="kube-filtering-label-template"></a>
## Filtering label templates by resource type
<!--PROCEDURE-->

Use optional fields in the ConfigMap's `data` section to apply labels and annotations only to specific resources.

**Procedure**

1. To apply labels only to a specific Kubernetes resource kind, add a `kind` field:

   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: deployment-labels
     labels:
       skupper.io/label-template: "true"
       deployment-tier: production
   data:
     kind: Deployment
   ```

   Valid values for `kind`: `Deployment`, `Service`, `ConfigMap`, `Secret`, `SecuredAccess`.

2. To apply labels only to a resource with a specific name, add a `name` field:

   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: router-labels
     labels:
       skupper.io/label-template: "true"
       component: router
   data:
     name: skupper-router
   ```

3. To apply labels only to resources matching a label selector, add a `labelSelector` field:

   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: listener-labels
     labels:
       skupper.io/label-template: "true"
     annotations:
       monitoring.io/scrape: "true"
   data:
     labelSelector: "internal.skupper.io/listener in (my-listener)"
   ```

   The `labelSelector` uses [Kubernetes label selector syntax](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors).
   If the selector is invalid, the entire template is ignored with a log warning.

4. To combine multiple filters (all must match):

   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: filtered-labels
     labels:
       skupper.io/label-template: "true"
       monitoring: enabled
   data:
     kind: Service
     labelSelector: "internal.skupper.io/listener in (my-listener)"
   ```

   This applies labels only to Service resources that match the label selector.

<a id="kube-excluding-keys"></a>
## Excluding specific keys from propagation
<!--PROCEDURE-->

Prevent certain labels or annotations from being propagated by listing them in the `exclude` field.

**Procedure**

1. Create a label template with an `exclude` field:

   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: selective-labels
     labels:
       skupper.io/label-template: "true"
       acme.com/propagate-me: "yes"
       internal-only: "do-not-copy"
     annotations:
       acme.com/public-annotation: "yes"
       internal-secret: "do-not-copy"
   data:
     exclude: "internal-only,internal-secret"
   ```

2. Apply the ConfigMap:

   ```bash
   kubectl apply -f selective-labels.yaml
   ```

   Only `acme.com/propagate-me` and `acme.com/public-annotation` are propagated to Skupper resources.
   The keys `internal-only` and `internal-secret` are excluded.

<a id="kube-multiple-label-templates"></a>
## Using multiple label templates
<!--CONCEPT-->

You can create multiple label template ConfigMaps in the same namespace.
All matching templates are applied.

**📌 NOTE**
If two templates set the same key to different values, the result is non-deterministic (last-write wins at reconcile time).
Avoid overlapping keys across templates unless the values are identical.

<a id="kube-label-template-lifecycle"></a>
## Managing label template lifecycle
<!--CONCEPT-->

Label templates are dynamic resources that affect Skupper-managed resources in real-time:

* **Create**: Labels and annotations are applied to existing and future Skupper resources immediately after the controller detects the ConfigMap.
* **Update**: Changing the ConfigMap's labels or annotations causes Skupper to reconcile and update affected resources.
* **Delete**: Removing the ConfigMap causes Skupper to remove the propagated labels and annotations from all affected resources.

<a id="kube-label-template-reference"></a>
## Label template reference
<!--REFERENCE-->

### Affected resources

The following Skupper-managed Kubernetes resources receive propagated labels and annotations:

| Resource kind | Example name |
| --- | --- |
| `Deployment` | `skupper-router` |
| `Service` | `skupper-router-local`, listener services |
| `ConfigMap` | Router configuration ConfigMap |
| `Secret` | TLS certificate secrets |
| `SecuredAccess` | Skupper CRD for router access |

### ConfigMap data fields

| Field | Type | Description |
| --- | --- | --- |
| `kind` | string | Filter by Kubernetes resource kind (`Deployment`, `Service`, `ConfigMap`, `Secret`, `SecuredAccess`) |
| `name` | string | Filter by exact resource name |
| `labelSelector` | string | Filter by existing labels using [Kubernetes label selector syntax](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors) |
| `exclude` | string | Comma-separated list of label/annotation keys to exclude from propagation |

All filters must match simultaneously (logical AND).

### Complete example

Apply custom labels to all Skupper Deployments and specific annotations only to the `skupper-router-local` Service:

```yaml
# Template 1: label all Skupper Deployments
apiVersion: v1
kind: ConfigMap
metadata:
  name: label-deployments
  labels:
    skupper.io/label-template: "true"
    acme.com/team: platform
    environment: staging
data:
  kind: Deployment
---
# Template 2: annotate the skupper-router-local Service only
apiVersion: v1
kind: ConfigMap
metadata:
  name: annotate-router-service
  labels:
    skupper.io/label-template: "true"
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
data:
  kind: Service
  name: skupper-router-local
```
