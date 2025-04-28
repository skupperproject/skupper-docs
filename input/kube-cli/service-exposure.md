<a id="kube-exposing-services-cli"></a>
# Exposing services on the application network using the CLI

After creating an application network by linking sites, you can expose services from one site using connectors and consume those services on other sites using listeners.
A *routing key* is a string that matches one or more connectors with one or more listeners.
For example, if you create a connector with the routing key `backend`, you need to create a listener with the routing key `backend` to consume that service.

This section assumes you have created and linked at least two sites.

<a id="kube-creating-connector-cli"></a>
<!-- Creating a connector on Kubernetes using the CLI -->
## Creating a connector using the CLI

A connector binds a local workload to listeners in remote sites.
Listeners and connectors are matched using routing keys.

For more information about connectors, see [Connector concept][connector].

**Procedure**

1. Create a workload that you want to expose on the network, for example:
   ```bash
   kubectl create deployment backend --image quay.io/skupper/hello-world-backend --replicas 3
   ```

2. Create a connector:
   ```bash
   skupper connector create <name> <port> [--routing-key <name>]
   ```
   For example:

   ```bash
   skupper connector create backend 8080 --workload deployment/backend
   ```
3. Check the connector status:
   ```bash
   skupper connector status
   ```
   
   For example:
   
   ```
   $ skupper connector status
   NAME    STATUS  ROUTING-KEY     SELECTOR        HOST    PORT    HAS MATCHING LISTENER    MESSAGE
   backend Pending backend         app=backend             8080    false   No matching listeners
   ```
   **📌 NOTE**
   By default, the routing key name is set to the name of the connector.
   If you want to use a custom routing key, set the `--routing-key` to your custom name.

There are many options to consider when creating connectors using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

**Additional information**

If you need to expose a service from another namespace, you must use YAML as described in [Creating a connector for a different namespace using YAML][attached].

<a id="kube-creating-listener-cli"></a>
<!-- Creating a listener on Kubernetes using the CLI -->
## Creating a listener using the CLI

A listener binds a local connection endpoint to connectors in remote sites. 
Listeners and connectors are matched using routing keys.

For more information about listeners. see [Listener concept][listener].

**Procedure**

1. Identify a connector that you want to use.
   Note the routing key of that connector.

2. Create a listener:
   ```bash
   skupper listener create <name> <port> [--routing-key <name>]
   ```
   For example:
   ```
   $ skupper listener create backend 8080
   Waiting for create to complete...
   Listener "backend" is ready
   ```

3. Check the listener status:
   ```bash
   skupper listener status
   ```
   
   For example:
   
   ```
   $ skupper listener status
   NAME    STATUS  ROUTING-KEY     HOST    PORT    MATCHING-CONNECTOR      MESSAGE
   backend Ready   backend         backend 8080    true                    OK
   ```
   
   **📌 NOTE**
   There must be a `MATCHING-CONNECTOR` for the service to operate.
   By default, the routing key name is the listener name.
   If you want to use a custom routing key, set the `--routing-key` to your custom name.

There are many options to consider when creating connectors using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.


[cli-ref]: https://skupperproject.github.io/refdog/commands/index.html
[connector]: https://skupperproject.github.io/refdog/concepts/connector.html
[listener]: https://skupperproject.github.io/refdog/concepts/listener.html
[attached]: ../kube-yaml/service-exposure.html#kube-creating-attachedconnector-yaml
