<a id="kube-exposing-services-cli"></a>
# Exposing services on the application network using the CLI on Kubernetes
<!--ASSEMBLY-->

Create connectors and listeners to expose services across the application network.

After creating an application network by linking sites, you can expose services from one site using connectors and consume those services on other sites using listeners.
A *routing key* is a string that matches one or more connectors with one or more listeners.
For example, if you create a connector with the routing key `backend`, you need to create a listener with the routing key `backend` to consume that service.

Before you begin, create and link at least two sites.

<a id="kube-creating-connector-cli"></a>
## Create a Kubernetes connector using the CLI
<!--PROCEDURE-->

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
   ```bash
   skupper connector status
   ```
   Example output:
   ```text
   NAME    STATUS  ROUTING-KEY     SELECTOR        HOST    PORT    HAS MATCHING LISTENER    MESSAGE
   backend Pending backend         app=backend             8080    false   No matching listeners
   ```

   > **NOTE:**
   > By default, the routing key name is set to the name of the connector.
   > If you want to use a custom routing key, set the `--routing-key` to your custom name.

**Additional resources**

* [CLI Reference][cli-ref]
* [Creating a connector for a different namespace using YAML][attached]

<a id="kube-creating-listener-cli"></a>
## Create a Kubernetes listener using the CLI
<!--PROCEDURE-->

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
   ```bash
   skupper listener create backend 8080
   ```
   Example output:
   ```text
   Waiting for create to complete...
   Listener "backend" is ready
   ```

3. Check the listener status:
   ```bash
   skupper listener status
   ```
   For example:
   ```bash
   skupper listener status
   ```
   Example output:
   ```text
   NAME    STATUS  ROUTING-KEY     HOST    PORT    MATCHING-CONNECTOR      MESSAGE
   backend Ready   backend         backend 8080    true                    OK
   ```

   > **NOTE:**
   > There must be a `MATCHING-CONNECTOR` for the service to operate.
   > By default, the routing key name is the listener name.
   > If you want to use a custom routing key, set the `--routing-key` to your custom name.

**Additional resources**

* [CLI Reference][cli-ref]

[cli-ref]: https://skupperproject.github.io/refdog/commands/index.html
[connector]: https://skupperproject.github.io/refdog/concepts/connector.html
[listener]: https://skupperproject.github.io/refdog/concepts/listener.html
[attached]: ../kube-yaml/service-exposure.html#kube-creating-attachedconnector-yaml
