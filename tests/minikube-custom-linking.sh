#!/usr/bin/env bash

set -euo pipefail

WEST_PROFILE="${WEST_PROFILE:-west}"
EAST_PROFILE="${EAST_PROFILE:-east}"
WEST_NAMESPACE="${WEST_NAMESPACE:-west}"
EAST_NAMESPACE="${EAST_NAMESPACE:-east}"
WORKDIR="${WORKDIR:-/tmp/skupper-docs-minikube-custom-linking}"
OUTPUT_DIR="${OUTPUT_DIR:-output/tests/minikube-custom-linking}"
START_PROFILES="${START_PROFILES:-1}"
START_TUNNEL="${START_TUNNEL:-1}"
TUNNEL_WITH_SUDO="${TUNNEL_WITH_SUDO:-0}"
PAUSE_ON_CHECKPOINTS="${PAUSE_ON_CHECKPOINTS:-1}"
PAUSE_ON_ERROR="${PAUSE_ON_ERROR:-1}"
INSTALL_SKUPPER="${INSTALL_SKUPPER:-1}"
SKUPPER_INSTALL_URL="${SKUPPER_INSTALL_URL:-https://skupper.io/install.yaml}"
MINIKUBE_DRIVER="${MINIKUBE_DRIVER:-}"
MINIKUBE_CPUS="${MINIKUBE_CPUS:-4}"
MINIKUBE_MEMORY="${MINIKUBE_MEMORY:-8192}"
TUNNEL_PID=""
TUNNEL_LOG=""
PROBE_POD_IMAGE="${PROBE_POD_IMAGE:-busybox:1.36}"

log() {
    printf '==> %s\n' "$*"
}

fail() {
    printf 'ERROR: %s\n' "$*" >&2

    if [[ "$PAUSE_ON_ERROR" == "1" && -t 0 ]]; then
        printf 'Press Enter to exit so you can inspect the cluster state... ' >&2
        read -r _
    fi

    exit 1
}

need_cmd() {
    command -v "$1" >/dev/null 2>&1 || fail "Missing required command: $1"
}

pause_checkpoint() {
    local message="$1"

    if [[ "$PAUSE_ON_CHECKPOINTS" != "1" || ! -t 0 ]]; then
        return
    fi

    printf '\nCheckpoint: %s\n' "$message"
    printf 'Press Enter to continue... '
    read -r _
}

west_kubectl() {
    kubectl --context="$WEST_PROFILE" --namespace="$WEST_NAMESPACE" "$@"
}

east_kubectl() {
    kubectl --context="$EAST_PROFILE" --namespace="$EAST_NAMESPACE" "$@"
}

skupper_api_available() {
    local context="$1"
    kubectl --context="$context" api-resources --api-group=skupper.io 2>/dev/null | grep -q '^sites'
}

start_profiles() {
    if [[ "$START_PROFILES" != "1" ]]; then
        log "Skipping minikube start because START_PROFILES=$START_PROFILES"
        return
    fi

    local west_start_args=(
        -p "$WEST_PROFILE"
        --cpus="$MINIKUBE_CPUS"
        --memory="$MINIKUBE_MEMORY"
    )
    local east_start_args=(
        -p "$EAST_PROFILE"
        --cpus="$MINIKUBE_CPUS"
        --memory="$MINIKUBE_MEMORY"
    )

    if [[ -n "$MINIKUBE_DRIVER" ]]; then
        west_start_args+=(--driver="$MINIKUBE_DRIVER")
        east_start_args+=(--driver="$MINIKUBE_DRIVER")
    fi

    log "Starting minikube profile $WEST_PROFILE"
    minikube start "${west_start_args[@]}"

    log "Starting minikube profile $EAST_PROFILE"
    minikube start "${east_start_args[@]}"
}

check_skupper_api() {
    log "Checking that the Skupper API is available on both clusters"

    if ! skupper_api_available "$WEST_PROFILE"; then
        if [[ "$INSTALL_SKUPPER" == "1" ]]; then
            install_skupper "$WEST_PROFILE"
        else
            fail "Skupper CRDs not found in context $WEST_PROFILE. Install the Skupper V2 controller in that cluster first."
        fi
    fi

    if ! skupper_api_available "$EAST_PROFILE"; then
        if [[ "$INSTALL_SKUPPER" == "1" ]]; then
            install_skupper "$EAST_PROFILE"
        else
            fail "Skupper CRDs not found in context $EAST_PROFILE. Install the Skupper V2 controller in that cluster first."
        fi
    fi
}

install_skupper() {
    local context="$1"
    local deadline
    deadline=$((SECONDS + 300))

    log "Installing Skupper in context $context from $SKUPPER_INSTALL_URL"
    kubectl --context="$context" apply -f "$SKUPPER_INSTALL_URL"

    log "Waiting for Skupper CRDs in context $context"
    while (( SECONDS < deadline )); do
        if skupper_api_available "$context"; then
            return
        fi
        sleep 5
    done

    fail "Timed out waiting for Skupper CRDs after install in context $context"
}

prepare_workdir() {
    rm -rf "$WORKDIR"
    mkdir -p "$WORKDIR"
    mkdir -p "$OUTPUT_DIR"
}

deploy_sites() {
    log "Creating namespaces"
    kubectl --context="$WEST_PROFILE" create namespace "$WEST_NAMESPACE" --dry-run=client -o yaml | kubectl --context="$WEST_PROFILE" apply -f -
    kubectl --context="$EAST_PROFILE" create namespace "$EAST_NAMESPACE" --dry-run=client -o yaml | kubectl --context="$EAST_PROFILE" apply -f -

    cat > "$OUTPUT_DIR/west-site.yaml" <<EOF
apiVersion: skupper.io/v2alpha1
kind: Site
metadata:
  name: ${WEST_NAMESPACE}
  namespace: ${WEST_NAMESPACE}
spec:
  linkAccess: default
EOF

    cat > "$OUTPUT_DIR/east-site.yaml" <<EOF
apiVersion: skupper.io/v2alpha1
kind: Site
metadata:
  name: ${EAST_NAMESPACE}
  namespace: ${EAST_NAMESPACE}
EOF

    log "Applying Site resources"
    kubectl --context="$WEST_PROFILE" apply -f "$OUTPUT_DIR/west-site.yaml"
    kubectl --context="$EAST_PROFILE" apply -f "$OUTPUT_DIR/east-site.yaml"
}

dump_site_diagnostics() {
    local context="$1"
    local namespace="$2"

    printf '\nDiagnostics for context=%s namespace=%s\n' "$context" "$namespace" >&2
    kubectl --context="$context" --namespace="$namespace" get site -o yaml >&2 || true
    kubectl --context="$context" --namespace="$namespace" get pods >&2 || true
    kubectl --context="$context" --namespace="$namespace" describe site "$namespace" >&2 || true
    kubectl --context="$context" --namespace="$namespace" get events --sort-by=.lastTimestamp >&2 || true
}

wait_for_site() {
    local context="$1"
    local namespace="$2"
    local deadline
    deadline=$((SECONDS + 300))

    log "Waiting for site $namespace in context $context"
    while (( SECONDS < deadline )); do
        if kubectl --context="$context" --namespace="$namespace" get site "$namespace" >/dev/null 2>&1; then
            local status
            status="$(kubectl --context="$context" --namespace="$namespace" get site "$namespace" --no-headers 2>/dev/null | awk '{print $2}')"
            if [[ "$status" == "Ready" ]]; then
                return
            fi
        fi
        sleep 5
    done

    dump_site_diagnostics "$context" "$namespace"
    fail "Timed out waiting for site $namespace in context $context"
}

wait_for_site_running() {
    local context="$1"
    local namespace="$2"
    local deadline
    deadline=$((SECONDS + 300))

    log "Waiting for site $namespace in context $context to be Running"
    while (( SECONDS < deadline )); do
        if kubectl --context="$context" --namespace="$namespace" get site "$namespace" >/dev/null 2>&1; then
            local running
            running="$(kubectl --context="$context" --namespace="$namespace" get site "$namespace" -o json | jq -r '.status.conditions[]? | select(.type=="Running") | .status')"
            if [[ "$running" == "True" ]]; then
                return
            fi
        fi
        sleep 5
    done

    dump_site_diagnostics "$context" "$namespace"
    fail "Timed out waiting for site $namespace in context $context to be Running"
}

prompt_for_tunnel() {
    if [[ "$START_TUNNEL" != "1" ]]; then
        return
    fi

    if [[ "$TUNNEL_WITH_SUDO" == "1" && "$EUID" -ne 0 ]]; then
        log "Requesting sudo access for minikube tunnel"
        sudo -v
    fi

    TUNNEL_LOG="$WORKDIR/minikube-tunnel.log"

    log "Starting minikube tunnel for profile $WEST_PROFILE"
    if [[ "$TUNNEL_WITH_SUDO" == "1" && "$EUID" -ne 0 ]]; then
        sudo --preserve-env=HOME,PATH minikube tunnel -p "$WEST_PROFILE" >"$TUNNEL_LOG" 2>&1 &
    else
        minikube tunnel -p "$WEST_PROFILE" >"$TUNNEL_LOG" 2>&1 &
    fi
    TUNNEL_PID=$!

    sleep 3
    if ! kill -0 "$TUNNEL_PID" >/dev/null 2>&1; then
        cat "$TUNNEL_LOG" >&2 || true
        fail "Failed to start minikube tunnel for profile $WEST_PROFILE"
    fi

    cat <<EOF

Started:

  minikube tunnel -p ${WEST_PROFILE}

Tunnel log:

  ${TUNNEL_LOG}
EOF
}

stop_tunnel() {
    if [[ -n "$TUNNEL_PID" ]] && kill -0 "$TUNNEL_PID" >/dev/null 2>&1; then
        log "Stopping minikube tunnel"
        kill "$TUNNEL_PID" >/dev/null 2>&1 || true
        wait "$TUNNEL_PID" 2>/dev/null || true
    fi
}

cleanup_probe_pod() {
    west_kubectl delete pod traffic-check --ignore-not-found=true >/dev/null 2>&1 || true
}

wait_for_endpoint_host() {
    local deadline
    deadline=$((SECONDS + 300))

    log "Waiting for a listening endpoint on ${WEST_PROFILE}/${WEST_NAMESPACE}"
    while (( SECONDS < deadline )); do
        WEST_HOST="$(west_kubectl get site "$WEST_NAMESPACE" -o json | jq -r '.status.endpoints[0].host // empty')"
        if [[ -n "$WEST_HOST" && "$WEST_HOST" != "null" ]]; then
            export WEST_HOST
            log "Using listening endpoint host: $WEST_HOST"
            return
        fi
        sleep 5
    done

    west_kubectl get site "$WEST_NAMESPACE" -o yaml || true
    fail "Timed out waiting for the listening endpoint. Ensure minikube tunnel is running for profile $WEST_PROFILE."
}

write_openssl_config() {
    local san_type="$1"
    local san_value="$2"

    cat > "$WORKDIR/server-ext.cnf" <<EOF
[req]
distinguished_name = dn
prompt = no

[dn]
CN = ${san_value}

[v3_server]
basicConstraints = CA:FALSE
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = ${san_type}:${san_value}
EOF

    cat > "$WORKDIR/client-ext.cnf" <<EOF
[req]
distinguished_name = dn
prompt = no

[dn]
CN = skupper-link

[v3_client]
basicConstraints = CA:FALSE
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = clientAuth
EOF
}

generate_certificates() {
    local san_type="DNS"
    if [[ "$WEST_HOST" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        san_type="IP"
    fi

    log "Generating a test CA, server certificate, and client certificate"
    write_openssl_config "$san_type" "$WEST_HOST"

    openssl genrsa -out "$WORKDIR/ca.key" 2048 >/dev/null 2>&1
    openssl req -x509 -new -nodes -key "$WORKDIR/ca.key" -sha256 -days 365 \
        -subj "/CN=skupper-docs-test-ca" \
        -out "$WORKDIR/ca.crt" >/dev/null 2>&1

    openssl genrsa -out "$WORKDIR/server.key" 2048 >/dev/null 2>&1
    openssl req -new -key "$WORKDIR/server.key" \
        -config "$WORKDIR/server-ext.cnf" \
        -out "$WORKDIR/server.csr" >/dev/null 2>&1
    openssl x509 -req -in "$WORKDIR/server.csr" \
        -CA "$WORKDIR/ca.crt" -CAkey "$WORKDIR/ca.key" -CAcreateserial \
        -out "$WORKDIR/server.crt" -days 365 -sha256 \
        -extfile "$WORKDIR/server-ext.cnf" -extensions v3_server >/dev/null 2>&1

    openssl genrsa -out "$WORKDIR/client.key" 2048 >/dev/null 2>&1
    openssl req -new -key "$WORKDIR/client.key" \
        -config "$WORKDIR/client-ext.cnf" \
        -out "$WORKDIR/client.csr" >/dev/null 2>&1
    openssl x509 -req -in "$WORKDIR/client.csr" \
        -CA "$WORKDIR/ca.crt" -CAkey "$WORKDIR/ca.key" -CAcreateserial \
        -out "$WORKDIR/client.crt" -days 365 -sha256 \
        -extfile "$WORKDIR/client-ext.cnf" -extensions v3_client >/dev/null 2>&1
}

write_secret_manifests() {
    local ca_b64 server_crt_b64 server_key_b64 client_crt_b64 client_key_b64
    ca_b64="$(base64 -w0 < "$WORKDIR/ca.crt")"
    server_crt_b64="$(base64 -w0 < "$WORKDIR/server.crt")"
    server_key_b64="$(base64 -w0 < "$WORKDIR/server.key")"
    client_crt_b64="$(base64 -w0 < "$WORKDIR/client.crt")"
    client_key_b64="$(base64 -w0 < "$WORKDIR/client.key")"

    cat > "$OUTPUT_DIR/skupper-site-server.yaml" <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: skupper-site-server
  namespace: ${WEST_NAMESPACE}
data:
  ca.crt: ${ca_b64}
  tls.crt: ${server_crt_b64}
  tls.key: ${server_key_b64}
EOF

    cat > "$OUTPUT_DIR/client-secret.yaml" <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: skupper-link
data:
  ca.crt: ${ca_b64}
  tls.crt: ${client_crt_b64}
  tls.key: ${client_key_b64}
EOF
}

apply_server_secret() {
    log "Applying the custom server certificate secret on the listening site"
    kubectl --context="$WEST_PROFILE" apply -f "$OUTPUT_DIR/skupper-site-server.yaml"
}

cleanup_stale_default_link_resources() {
    log "Removing any stale skupper-link resources from the default namespace on the connecting site"
    kubectl --context="$EAST_PROFILE" --namespace=default delete link skupper-link --ignore-not-found=true >/dev/null 2>&1 || true
    kubectl --context="$EAST_PROFILE" --namespace=default delete secret skupper-link --ignore-not-found=true >/dev/null 2>&1 || true
}

build_link_bundle() {
    log "Building the Link YAML using kubectl, jq, and yq"
    local endpoints
    endpoints="$(west_kubectl get site "$WEST_NAMESPACE" -o json | jq -c '.status.endpoints')"
    printf '%s\n' "$endpoints" | jq '.' > "$OUTPUT_DIR/west-endpoints.json"

    cat > "$OUTPUT_DIR/west-link-template.json" <<EOF
{
  "apiVersion": "skupper.io/v2alpha1",
  "kind": "Link",
  "metadata": {
    "name": "skupper-link"
  },
  "spec": {
    "cost": 1,
    "tlsCredentials": "skupper-link"
  }
}
EOF

    jq --argjson endpoints "$endpoints" '.spec.endpoints = $endpoints' \
        "$OUTPUT_DIR/west-link-template.json" > "$OUTPUT_DIR/west-link-rendered.json"

    yq eval -P -o=yaml "$OUTPUT_DIR/west-link-rendered.json" > "$OUTPUT_DIR/west-link.yaml"

    printf '%s\n' '---' >> "$OUTPUT_DIR/west-link.yaml"
    cat "$OUTPUT_DIR/client-secret.yaml" >> "$OUTPUT_DIR/west-link.yaml"
}

apply_link_bundle() {
    log "Applying the Link bundle on the connecting site"
    cleanup_stale_default_link_resources
    east_kubectl apply -f "$OUTPUT_DIR/west-link.yaml"
}

deploy_backend_workload() {
    log "Deploying a backend workload on the connecting site"
    cat > "$OUTPUT_DIR/backend-deployment.yaml" <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: ${EAST_NAMESPACE}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: quay.io/skupper/hello-world-backend
          ports:
            - containerPort: 8080
EOF
    kubectl --context="$EAST_PROFILE" apply -f "$OUTPUT_DIR/backend-deployment.yaml"
    kubectl --context="$EAST_PROFILE" --namespace="$EAST_NAMESPACE" rollout status deployment/backend --timeout=300s
}

apply_service_exposure_resources() {
    log "Applying Skupper v2 Connector and Listener resources"
    cat > "$OUTPUT_DIR/backend-connector.yaml" <<EOF
apiVersion: skupper.io/v2alpha1
kind: Connector
metadata:
  name: backend
  namespace: ${EAST_NAMESPACE}
spec:
  routingKey: backend
  selector: app=backend
  port: 8080
EOF

    cat > "$OUTPUT_DIR/backend-listener.yaml" <<EOF
apiVersion: skupper.io/v2alpha1
kind: Listener
metadata:
  name: backend
  namespace: ${WEST_NAMESPACE}
spec:
  routingKey: backend
  host: east-backend
  port: 8080
EOF

    kubectl --context="$EAST_PROFILE" apply -f "$OUTPUT_DIR/backend-connector.yaml"
    kubectl --context="$WEST_PROFILE" apply -f "$OUTPUT_DIR/backend-listener.yaml"
}

wait_for_link_ready() {
    local deadline
    deadline=$((SECONDS + 300))

    log "Waiting for the link to become Ready"
    while (( SECONDS < deadline )); do
        if east_kubectl get link skupper-link >/dev/null 2>&1; then
            local status
            status="$(east_kubectl get link skupper-link --no-headers 2>/dev/null | awk '{print $2}')"
            if [[ "$status" == "Ready" ]]; then
                east_kubectl get link
                return
            fi
        fi
        sleep 5
    done

    printf '\nDiagnostics for link readiness in context=%s namespace=%s\n' "$EAST_PROFILE" "$EAST_NAMESPACE" >&2
    east_kubectl get link -o yaml >&2 || true
    kubectl --context="$EAST_PROFILE" get link -A >&2 || true
    east_kubectl get secret skupper-link -o yaml >&2 || true
    east_kubectl get events --sort-by=.lastTimestamp >&2 || true
    fail "Timed out waiting for link skupper-link to become Ready"
}

wait_for_service_exposure_ready() {
    local deadline
    deadline=$((SECONDS + 300))

    log "Waiting for Connector and Listener resources to become Ready"
    while (( SECONDS < deadline )); do
        local connector_status listener_status
        connector_status="$(east_kubectl get connector backend --no-headers 2>/dev/null | awk '{print $2}')"
        listener_status="$(west_kubectl get listener backend --no-headers 2>/dev/null | awk '{print $5}')"

        if [[ "$connector_status" == "Ready" && "$listener_status" == "Ready" ]]; then
            east_kubectl get connector
            west_kubectl get listener
            return
        fi
        sleep 5
    done

    east_kubectl get connector || true
    west_kubectl get listener || true
    fail "Timed out waiting for Connector and Listener resources to become Ready"
}

verify_remote_traffic() {
    local deadline
    deadline=$((SECONDS + 300))

    log "Verifying cross-site traffic through the Listener service"
    cleanup_probe_pod
    west_kubectl run traffic-check --image="$PROBE_POD_IMAGE" --restart=Never --command -- sh -c 'sleep 3600'
    west_kubectl wait --for=condition=Ready pod/traffic-check --timeout=180s

    while (( SECONDS < deadline )); do
        if west_kubectl exec traffic-check -- wget -qO- http://east-backend:8080/ > "$WORKDIR/traffic-check-response.txt" 2>/dev/null; then
            log "Traffic check succeeded"
            cat "$WORKDIR/traffic-check-response.txt"
            cleanup_probe_pod
            return
        fi
        sleep 5
    done

    west_kubectl get svc east-backend || true
    cleanup_probe_pod
    fail "Timed out verifying traffic through service east-backend"
}

print_summary() {
    cat <<EOF

Artifacts are in:
  ${WORKDIR}

YAML artifacts are in:
  ${OUTPUT_DIR}

Key files:
  ${OUTPUT_DIR}/west-site.yaml
  ${OUTPUT_DIR}/east-site.yaml
  ${OUTPUT_DIR}/skupper-site-server.yaml
  ${OUTPUT_DIR}/client-secret.yaml
  ${OUTPUT_DIR}/west-endpoints.json
  ${OUTPUT_DIR}/west-link-template.json
  ${OUTPUT_DIR}/west-link-rendered.json
  ${OUTPUT_DIR}/west-link.yaml
  ${OUTPUT_DIR}/backend-deployment.yaml
  ${OUTPUT_DIR}/backend-connector.yaml
  ${OUTPUT_DIR}/backend-listener.yaml
  ${WORKDIR}/traffic-check-response.txt

Useful follow-up checks:
  kubectl --context=${WEST_PROFILE} -n ${WEST_NAMESPACE} get site -o yaml | yq eval -o=yaml '.status.endpoints' -
  kubectl --context=${EAST_PROFILE} -n ${EAST_NAMESPACE} get link -o yaml
  kubectl --context=${EAST_PROFILE} -n ${EAST_NAMESPACE} get connector -o yaml
  kubectl --context=${WEST_PROFILE} -n ${WEST_NAMESPACE} get listener -o yaml
EOF
}

cleanup() {
    pause_checkpoint "About to delete the minikube profiles, namespaces, and generated files"
    cleanup_probe_pod
    stop_tunnel
    log "Deleting namespaces and minikube profiles"
    kubectl --context="$WEST_PROFILE" delete namespace "$WEST_NAMESPACE" --ignore-not-found=true || true
    kubectl --context="$EAST_PROFILE" delete namespace "$EAST_NAMESPACE" --ignore-not-found=true || true
    minikube delete -p "$WEST_PROFILE" || true
    minikube delete -p "$EAST_PROFILE" || true
    rm -rf "$WORKDIR"
}

usage() {
    cat <<EOF
Usage:
  $0 all
  $0 cleanup

Environment overrides:
  WEST_PROFILE, EAST_PROFILE
  WEST_NAMESPACE, EAST_NAMESPACE
  WORKDIR
  OUTPUT_DIR
  START_PROFILES=0     Skip 'minikube start'
  START_TUNNEL=0       Do not start 'minikube tunnel'
  TUNNEL_WITH_SUDO=0   Run 'minikube tunnel' without sudo
  PAUSE_ON_CHECKPOINTS=0  Disable interactive Enter-to-continue checkpoints
  PAUSE_ON_ERROR=0     Do not pause before exiting on error
  INSTALL_SKUPPER=0    Do not auto-install Skupper when CRDs are missing
  SKUPPER_INSTALL_URL  Skupper install manifest URL
  PROBE_POD_IMAGE      Override the probe image used for the traffic check
  MINIKUBE_DRIVER      Optional. If unset, minikube auto-detects the driver
  MINIKUBE_CPUS, MINIKUBE_MEMORY
EOF
}

main() {
    local action="${1:-all}"

    trap stop_tunnel EXIT

    need_cmd minikube
    need_cmd kubectl
    need_cmd jq
    need_cmd yq
    need_cmd openssl
    need_cmd base64
    need_cmd grep
    need_cmd awk

    case "$action" in
        all)
            prepare_workdir
            start_profiles
            check_skupper_api
            deploy_sites
            wait_for_site_running "$WEST_PROFILE" "$WEST_NAMESPACE"
            wait_for_site_running "$EAST_PROFILE" "$EAST_NAMESPACE"
            pause_checkpoint "Both Skupper sites are running"
            prompt_for_tunnel
            wait_for_site "$WEST_PROFILE" "$WEST_NAMESPACE"
            wait_for_endpoint_host
            generate_certificates
            write_secret_manifests
            apply_server_secret
            build_link_bundle
            apply_link_bundle
            wait_for_link_ready
            pause_checkpoint "The custom-certificate Link is ready"
            deploy_backend_workload
            apply_service_exposure_resources
            wait_for_service_exposure_ready
            verify_remote_traffic
            pause_checkpoint "Everything is running and end-to-end traffic succeeded"
            print_summary
            ;;
        cleanup)
            cleanup
            ;;
        *)
            usage
            exit 1
            ;;
    esac
}

main "$@"
