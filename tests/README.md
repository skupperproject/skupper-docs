# Tests

This directory contains ad hoc test helpers for validating documentation procedures locally.

## Minikube custom-link test

`minikube-custom-linking.sh` exercises the Kubernetes YAML workflow for linking two Skupper sites with:

* two Minikube profiles
* a custom `skupper-site-server` certificate on the listening site
* a manually generated client `Secret`
* a `Link` YAML file assembled with `kubectl`, `jq`, and `yq`
* a V2 `Connector` and `Listener` pair to validate service exposure

The script is intended for Fedora and assumes:

* `minikube`
* `kubectl`
* `jq`
* `mikefarah/yq` v4
* `openssl`
* access to download the Skupper install manifest unless Skupper is already installed

### What it does

1. Starts Minikube profiles `west` and `east` unless `START_PROFILES=0`.
2. Installs Skupper automatically with `kubectl apply -f https://skupper.io/install.yaml` if the CRDs are missing.
3. Creates `Site` resources in namespaces `west` and `east`.
4. Waits for both sites to reach the `Running` condition.
5. Starts `minikube tunnel -p west` automatically and writes its output to a log file.
6. Waits for the `west` site to become fully `Ready` and expose a listening endpoint.
7. Generates a temporary CA, server certificate, and client certificate.
8. Applies a custom `skupper-site-server` secret on the listening site.
9. Builds `west-link.yaml` using the same `jq` and `yq` pattern described in the docs.
10. Applies the generated link bundle in the `east` namespace and waits for the link to become `Ready`.
11. Deploys `quay.io/skupper/hello-world-backend` on the `east` site.
12. Applies a V2 `Connector` on `east` and a V2 `Listener` on `west`.
13. Starts a probe pod on `west` and fetches `http://east-backend:8080/` through the application network.
14. Pauses at a few checkpoints so you can inspect the clusters before continuing.

### Usage

Start the test:

```bash
./tests/minikube-custom-linking.sh
```

If the Minikube profiles already exist:

```bash
START_PROFILES=0 ./tests/minikube-custom-linking.sh
```

Skip automatic tunnel startup:

```bash
START_TUNNEL=0 ./tests/minikube-custom-linking.sh
```

Disable the interactive checkpoints:

```bash
PAUSE_ON_CHECKPOINTS=0 ./tests/minikube-custom-linking.sh
```

Disable the pause before exit on failures:

```bash
PAUSE_ON_ERROR=0 ./tests/minikube-custom-linking.sh
```

Skip automatic Skupper installation:

```bash
INSTALL_SKUPPER=0 ./tests/minikube-custom-linking.sh
```

Clean up the namespaces, profiles, and generated files:

```bash
./tests/minikube-custom-linking.sh cleanup
```

### Notes

* By default the script starts `minikube tunnel -p west` itself without `sudo`. Set `TUNNEL_WITH_SUDO=1` only if your local Minikube setup requires it.
* By default the script lets Minikube auto-detect the driver. Set `MINIKUBE_DRIVER` only if you need to force a specific driver on your machine.
* By default the script installs Skupper from `https://skupper.io/install.yaml` if the CRDs are missing. Override `SKUPPER_INSTALL_URL` if you want to use a different manifest.
* The script writes generated YAML manifests to `output/tests/minikube-custom-linking` unless `OUTPUT_DIR` is set.
* The script also saves the `Link` generation intermediates there, including the raw endpoint JSON, the JSON template, and the rendered JSON before conversion to YAML.
* The script writes transient files such as certificates, logs, and traffic output to `/tmp/skupper-docs-minikube-custom-linking` unless `WORKDIR` is set.
* The tunnel output is written to `${WORKDIR}/minikube-tunnel.log`.
* By default the script pauses for Enter at a few Skupper-related checkpoints, including after both sites are running, after the link is ready, and after service traffic is working. Set `PAUSE_ON_CHECKPOINTS=0` to disable that behavior.
* By default the script also pauses before exiting on an error so you can inspect the cluster state while the resources and tunnel are still up. Set `PAUSE_ON_ERROR=0` to disable that behavior.
* The script validates the manual client-secret path from the YAML documentation. It does not exercise the `Certificate` resource variant.
* By default the traffic check uses `busybox:1.36` and `wget`. Override `PROBE_POD_IMAGE` if you need a different probe image in your environment.
* `cleanup` removes the Minikube profiles and the temporary work directory, but it does not remove the saved YAML files under `output/`.
