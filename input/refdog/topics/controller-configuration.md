---
render_macros: false
---

# Controller configuration

The controller configuration controls two aspects at present: the
access types supported and their configuration, and whether the grant
server is enabled and how it is configured.

Access type configuration:

| Option | Description |
| :---- | :---- |
| `-default-access-type` | The default access type. |
| `-enabled-access-types` | The access types which should be enabled for sites to choose from. (default `local,loadbalancer,route`) |
| `-cluster-host` | The hostname or IP address through which the cluster can be reached. Required for configuring nodeport as an access type. |
| `-ingress-domain` | The domain to use in constructing the fully qualified hostname for Ingress resources, through which the ingress controller can be reached. Only used when selecting `ingress-nginx` as an access type. |
| `-http-proxy-domain` | The domain to use in constructing the fully qualified hostname for contour HttpProxy resources, through which the contour controller can be reached. Only used when selecting `contour-http-proxy` as an access type. |
| `-gateway-class` | The class of Gateway to use. This is required to enable `gateway` as an access type. |
| `-gateway-domain` | The domain to use in constructing the fully qualified hostname for TLSRoutes resources. Only used when selecting `gateway` as an access type. |
| `-gateway-port` | The port the Gateway should be configured to listen on. This is only used if `gateway` is enabled as an access type. (default 8443)  |

Grant server configuration:

| Option | Description |
| :---- | :---- |
| `-enable-grants` | Enable use of AccessGrants. |
| `-grant-server-autoconfigure` | Automatically configure the URL and TLS credentials for the AccessGrant Server. |
| `-grant-server-base-url` | The base url through which the AccessGrant server can be reached. |
| `-grant-server-port`  | The port on which the AccessGrant server should listen. (default 9090) |
| `-grant-server-tls-credentials` | The name of a secret in which TLS credentials for the AccessGrant server are found. (default `skupper-grant-server`) |
| `-grant-server-podname` | The name of the pod in which the AccessGrant server is running (default `$HOSTNAME`) |
