<a id="observer-config"></a>
<!--REFERENCE-->
# Network Observer Configuration Reference

Complete reference of all configuration options for the Skupper Network Observer. These options apply to both Helm chart deployments (`values.yaml`) and Operator-managed Custom Resource deployments (`spec` field).

> **Deployment guides:** See the Helm deployment guide for format-specific examples.

## Configuration Path Format

| Deployment Method | Configuration Path |
|-------------------|-------------------|
| **Helm** | Direct path in `values.yaml` |
| **Operator** | Same path under `spec:` in NetworkObserver CR |

**Example:**

```yaml
# Helm values.yaml
auth:
  strategy: basic

# NetworkObserver CR
spec:
  auth:
    strategy: basic
```

<a id="observer-external-access"></a>
## External Access

### Ingress

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `ingress.enabled` | bool | `false` | Enable Kubernetes Ingress resource |
| `ingress.className` | string | `""` | IngressClass name (e.g., `nginx`, `traefik`) |
| `ingress.annotations` | map | `{}` | Annotations for Ingress resource |
| `ingress.hosts` | array | `[]` | Host configurations |
| `ingress.hosts[].host` | string | - | Hostname |
| `ingress.hosts[].paths` | array | - | Path configurations |
| `ingress.hosts[].paths[].path` | string | - | URL path |
| `ingress.hosts[].paths[].pathType` | string | - | `Prefix`, `Exact`, or `ImplementationSpecific` |
| `ingress.tls` | array | `[]` | TLS configurations |
| `ingress.tls[].secretName` | string | - | TLS certificate Secret name |
| `ingress.tls[].hosts` | array | - | Hostnames for this certificate |

**Notes:**
- Backend always uses HTTPS (re-encryption required)
- Controller must support TLS backend

### Route (OpenShift)

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `route.enabled` | bool | `false` | Enable OpenShift Route resource |
| `route.host` | string | `""` | Explicit hostname |
| `route.subdomain` | string | `""` | Subdomain for automatic FQDN |
| `route.annotations` | map | `{}` | Route annotations |
| `route.labels` | map | `{}` | Route labels |

**Notes:**
- Automatically uses `reencrypt` TLS termination
- Use `host` OR `subdomain`, not both
- OpenShift only

<a id="observer-authentication"></a>
## Authentication

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `auth.strategy` | string | `"basic"` | Authentication strategy: `basic`, `openshift`, `none` |

### Basic Authentication

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `auth.basic.create` | bool | `true` | Auto-generate htpasswd Secret with random password |
| `auth.basic.secretName` | string | `""` | Existing htpasswd Secret name (requires `htpasswd` key) |

**Generated credentials:**
- Username: `skupper`
- Password: Random 16-character string (stored in Secret)

### OpenShift OAuth

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `auth.openshift.createCookieSecret` | bool | `true` | Auto-generate session cookie secret |
| `auth.openshift.cookieSecretName` | string | `""` | Existing cookie Secret name |
| `auth.openshift.serviceAccount.create` | bool | `true` | Create ServiceAccount for OAuth |
| `auth.openshift.serviceAccount.nameOverride` | string | `""` | Custom ServiceAccount name |

**Requirements:**
- OpenShift cluster
- RBAC permissions for delegated authentication

<a id="observer-tls"></a>
## TLS Certificates

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `tls.skupperIssued` | bool | `true` | Use Skupper controller CA (default) |
| `tls.openshiftIssued` | bool | `false` | Use OpenShift Service CA |
| `tls.secretName` | string | `""` | Existing TLS Secret name |

**Priority:** `secretName` > `openshiftIssued` > `skupperIssued`

**Methods:**
- **Skupper-issued:** Auto-provisioned by controller, uses same CA as inter-site links
- **OpenShift Service CA:** Platform-issued, automatic rotation
- **External:** Manual management, Secret type `kubernetes.io/tls`

<a id="observer-router"></a>
## Router Connection

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `router.endpoint` | string | `"amqps://skupper-router-local"` | AMQP endpoint URL |
| `router.certificate.create` | bool | `true` | Auto-create client certificate |
| `router.certificate.nameOverride` | string | `""` | Custom certificate name |

**Notes:**
- Endpoint must use `amqps://` scheme
- Client certificate provisioned by Skupper controller
- Certificate mounted at `/etc/messaging/`

<a id="observer-tuning"></a>
## Network Observer Tuning

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `extraArgs` | array | `[]` | Command-line flags for observer container |

**Available flags:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-enable-console` | bool | `true` | Enable web console UI |
| `-flow-record-ttl` | duration | `15m` | Flow record retention time |
| `-cors-allow-all` | bool | `false` | Allow all CORS origins (dev only) |
| `-vanflow-logging-profile` | string | `silent` | Vanflow logging: `silent`, `minimal`, `moderate`, `all` |

**Example:**
```yaml
extraArgs:
  - -flow-record-ttl=1h
  - -vanflow-logging-profile=minimal
```

<a id="observer-prometheus"></a>
## Prometheus Configuration

The Prometheus container supports custom configuration and tuning options.

### Configuration File

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `prometheus.config` | string | embedded | Complete `prometheus.yml` content |

**Default scrape config:**
```yaml
scrape_configs:
  - job_name: 'network-observer'
    static_configs:
      - targets: ['localhost:8080']
```

### Command-Line Flags

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `prometheus.extraArgs` | array | `[]` | Additional Prometheus flags |

**Common flags:**
- `--storage.tsdb.retention.time=<duration>`
- `--storage.tsdb.retention.size=<bytes>`
- `--query.max-samples=<int>`

**Example:**

```yaml
prometheus:
  extraArgs:
    - --storage.tsdb.retention.time=15d
    - --storage.tsdb.retention.size=10GB
```

### Extra Volumes and Mounts

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `prometheus.extraVolumes` | array | `[]` | Additional volumes (Kubernetes volume spec) |
| `prometheus.extraVolumeMounts` | array | `[]` | Volume mount points (Kubernetes volumeMount spec) |

**Example:**

```yaml
prometheus:
  extraVolumes:
    - name: extra-config
      configMap:
        name: prometheus-rules
  extraVolumeMounts:
    - name: extra-config
      mountPath: /etc/prometheus/rules
```

<a id="observer-persistence"></a>
## Data Persistence

By default, Prometheus uses ephemeral storage (`emptyDir`). For persistent time-series data, enable a PersistentVolumeClaim.

### Persistence Options

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `prometheus.persistence.enabled` | bool | `false` | Enable persistent storage |
| `prometheus.persistence.storageClass` | string | `""` | StorageClass name (empty = default) |
| `prometheus.persistence.size` | string | `8Gi` | PVC size |
| `prometheus.persistence.accessModes` | array | `["ReadWriteOnce"]` | PVC access modes |

**Behavior:**
- Disabled: Uses `emptyDir` (ephemeral)
- Enabled: Creates PVC, uses `Recreate` deployment strategy

**Prerequisites**

* A StorageClass that can provision PersistentVolumes, or a default StorageClass configured in your cluster

**Procedure**

1. Configure persistence in your values file:

   ```yaml
   prometheus:
     persistence:
       enabled: true
       storageClass: ""   # Use default StorageClass
       size: 8Gi
       accessModes:
         - ReadWriteOnce
   ```

2. Install or upgrade the chart with your values:

   ```bash
   helm upgrade --install skupper-network-observer oci://quay.io/skupper/helm/network-observer --version {{skupper_cli_version}} -f values.yaml
   ```

3. Verify the PersistentVolumeClaim is bound:

   ```bash
   kubectl get pvc
   ```

   Example output:

   ```text
   NAME                                    STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
   skupper-network-observer-prometheus-0   Bound    pvc-a1b2c3d4-e5f6-7890-abcd-ef1234567890   8Gi        RWO            standard       2m
   ```

**Important:** When persistence is enabled, the Deployment uses a **Recreate** update strategy to ensure the single read-write volume can attach cleanly during pod updates.

<a id="observer-resources"></a>
## Container Resources

Resource requests and limits can be configured for each container in the Pod.

### Network Observer Container

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `containerResources.networkObserver.requests.cpu` | string | - | CPU request |
| `containerResources.networkObserver.requests.memory` | string | - | Memory request |
| `containerResources.networkObserver.limits.cpu` | string | - | CPU limit |
| `containerResources.networkObserver.limits.memory` | string | - | Memory limit |

### Prometheus Container

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `containerResources.prometheus.requests.cpu` | string | - | CPU request |
| `containerResources.prometheus.requests.memory` | string | - | Memory request |
| `containerResources.prometheus.limits.cpu` | string | - | CPU limit |
| `containerResources.prometheus.limits.memory` | string | - | Memory limit |

### Proxy Container

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `containerResources.proxy.requests.cpu` | string | - | CPU request |
| `containerResources.proxy.requests.memory` | string | - | Memory request |
| `containerResources.proxy.limits.cpu` | string | - | CPU limit |
| `containerResources.proxy.limits.memory` | string | - | Memory limit |

**Example:**

```yaml
containerResources:
  networkObserver:
    requests:
      cpu: 200m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi
  prometheus:
    requests:
      cpu: 500m
      memory: 1Gi
    limits:
      cpu: 2000m
      memory: 4Gi
  proxy:
    requests:
      cpu: 50m
      memory: 64Mi
    limits:
      cpu: 200m
      memory: 256Mi
```

<a id="observer-images"></a>
## Container Images

### Network Observer Image

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `image.repository` | string | `quay.io/skupper/network-observer` | Image repository |
| `image.tag` | string | chart appVersion | Image tag |
| `image.pullPolicy` | string | `Always` | Pull policy |

### Prometheus Image

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `prometheus.repository` | string | `quay.io/prometheus/prometheus` | Image repository |
| `prometheus.tag` | string | `v3.11.3` | Image tag |
| `prometheus.pullPolicy` | string | `IfNotPresent` | Pull policy |

### NGINX Proxy Image

Used when `auth.strategy` is `basic` or `none`:

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `nginx.repository` | string | `mirror.gcr.io/nginxinc/nginx-unprivileged` | Image repository |
| `nginx.tag` | string | `1.31.0-alpine` | Image tag |
| `nginx.pullPolicy` | string | `IfNotPresent` | Pull policy |
| `nginx.command` | array | `[]` | Override default command |

### OpenShift OAuth Proxy Image

Used when `auth.strategy` is `openshift`:

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `openshiftOauthProxy.repository` | string | `quay.io/openshift/origin-oauth-proxy` | Image repository |
| `openshiftOauthProxy.tag` | string | `4.22.0` | Image tag |
| `openshiftOauthProxy.pullPolicy` | string | `IfNotPresent` | Pull policy |

<a id="observer-labels"></a>
## Labels and Annotations

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `commonLabels` | map | `{}` | Labels on all resources |
| `commonAnnotations` | map | `{}` | Annotations on all resources |
| `podLabels` | map | `{}` | Labels on Pod resources only |
| `podAnnotations` | map | `{}` | Annotations on Pod resources only |

**Standard labels (always present):**
- `app.kubernetes.io/name: network-observer`
- `app.kubernetes.io/instance: <name>`
- `app.kubernetes.io/version: <version>`
- `app.kubernetes.io/managed-by: Helm` or `network-observer-operator`

**Example:**

```yaml
commonLabels:
  environment: production
  team: platform-engineering
  cost-center: "12345"

commonAnnotations:
  owner: "platform-team@company.com"
  docs: "https://wiki.company.com/network-observer"

podLabels:
  app.kubernetes.io/tier: monitoring

podAnnotations:
  prometheus.io/scrape: "false"
```

<a id="observer-service"></a>
## Service

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `service.type` | string | `ClusterIP` | Service type: `ClusterIP`, `LoadBalancer`, `NodePort` |
| `service.port` | int | `443` | External port |

**Notes:**
- `targetPort` always `https` (8443)
- Metrics service always `ClusterIP` on port `9000`

<a id="observer-security"></a>
## Security

### Pod Security Context

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `podSecurityContext.seccompProfile.type` | string | `RuntimeDefault` | Seccomp profile |

### Container Security Contexts

Available for: `securityContext`, `prometheus.securityContext`, `nginx.securityContext`, `openshiftOauthProxy.securityContext`

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `.allowPrivilegeEscalation` | bool | `false` | Allow privilege escalation |
| `.capabilities.drop` | array | `["ALL"]` | Capabilities to drop |

<a id="observer-advanced"></a>
## Advanced Options

### Name Overrides

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `nameOverride` | string | `""` | Override chart name |
| `fullnameOverride` | string | `""` | Override full resource name |

### Skip Management Labels

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `skipManagementLabels` | bool | `false` | Skip Skupper management labels |

<a id="observer-metrics"></a>
## Metrics Endpoint

The Network Observer serves Prometheus metrics on a dedicated HTTP listener, separate from the main API endpoint.

**Listener Configuration:**
- Address: `:9000` (container-wide)
- Path: `/metrics`
- Protocol: HTTP (no TLS/auth)

**Service:**
- Name: `<name>-metrics`
- Type: `ClusterIP`
- Port: `9000 → 9000`

**Security:** Cluster-internal only. Do not expose publicly.

### Metrics Service

The chart creates a second ClusterIP Service named `<release-name>-metrics` that targets the metrics listener on port **9000**.

| Property | Value |
|----------|-------|
| **Listener address** | `:9000` |
| **Service name** | `<release-name>-metrics` |
| **Service port** | `9000` |
| **Metrics path** | `/metrics` |

### Scraping Metrics

Configure your Prometheus instance or monitoring operator to scrape the metrics endpoint.

**ServiceMonitor example (Prometheus Operator):**

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: skupper-network-observer
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: network-observer
  endpoints:
    - port: metrics
      path: /metrics
```

**Static scrape configuration:**

```yaml
scrape_configs:
  - job_name: 'network-observer'
    static_configs:
      - targets: ['skupper-network-observer-metrics.default.svc:9000']
```

**Security note:** The metrics Service is **ClusterIP** by default and does not include the TLS proxy or authentication that protects the main console endpoint. Do not expose this Service publicly without additional access controls if your metrics contain sensitive data.

<a id="observer-validation"></a>
## Validation and Troubleshooting

### Verify Services

Check that both Services are created:

```bash
kubectl get svc -l app.kubernetes.io/name=network-observer
```

Example output:

```text
NAME                              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
skupper-network-observer          ClusterIP   10.96.123.45    <none>        443/TCP    5m
skupper-network-observer-metrics  ClusterIP   10.96.123.46    <none>        9000/TCP   5m
```

### Test Metrics Endpoint

From a pod in the same namespace:

```bash
kubectl run -it --rm curl --image=curlimages/curl --restart=Never -- curl -sS http://skupper-network-observer-metrics:9000/metrics
```

Example output:

```text
# HELP skupper_network_observer_info Network Observer build information
# TYPE skupper_network_observer_info gauge
skupper_network_observer_info{version="2.2.0"} 1
...
```

### Check Observer Logs

Look for the metrics listener startup message:

```bash
kubectl logs deployment/skupper-network-observer -c network-observer
```

Example output:

```text
2025/03/15 10:23:45 Starting metrics server on :9000
2025/03/15 10:23:45 Starting API server on 127.0.0.1:8080
```

### Verify Prometheus Configuration

If the embedded Prometheus shows no data, check the ConfigMap:

```bash
kubectl get configmap skupper-network-observer-prometheus-config -o yaml
```

Ensure the `prometheus.yml` content is valid and the scrape target matches the observer's API listener (`localhost:8080`).

### PersistentVolumeClaim Issues

If the pod remains in `Pending` state with persistence enabled:

```bash
kubectl describe pvc skupper-network-observer-prometheus-0
```

Look for events indicating StorageClass issues, volume provisioning failures, or capacity constraints.
