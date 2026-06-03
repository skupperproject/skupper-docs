<a id="observer-config"></a>
<!--REFERENCE-->
# Network Observer configuration options

The Network Observer supports advanced configuration options for Prometheus monitoring and metrics collection.

<a id="observer-prometheus"></a>
## Prometheus Configuration

The Prometheus container supports custom configuration and tuning options.

### Custom Prometheus Configuration

By default, the chart uses an embedded `prometheus.yml` configuration. You can supply a complete custom configuration using the `prometheus.config` parameter.

```yaml
prometheus:
  config: |
    global:
      scrape_interval: 15s
    scrape_configs:
      - job_name: 'network-observer'
        static_configs:
          - targets: ['localhost:8080']
```

### Prometheus Process Flags

Additional Prometheus command-line flags can be appended using `prometheus.extraArgs`.

```yaml
prometheus:
  extraArgs:
    - --storage.tsdb.retention.time=15d
    - --storage.tsdb.retention.size=10GB
```

### Extra Volumes and Mounts

Additional volumes can be attached to the Prometheus container using `prometheus.extraVolumes` and `prometheus.extraVolumeMounts`.

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

<a id="observer-metrics"></a>
## Metrics Endpoint

The Network Observer serves Prometheus metrics on a dedicated HTTP listener, separate from the main API endpoint.

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
