<a id="system-yaml-service-exposure"></a>
# Exposing services on the application network using YAML
<!--ASSEMBLY-->

Use YAML to create connectors and listeners for services on the application network.

After creating an application network by linking sites, you can expose services from one site using connectors and consume those services on other sites using listeners.
A *routing key* is a string that matches one or more connectors with one or more listeners.
For example, if you create a connector with the routing key `backend`, you need to create a listener with the routing key `backend` to consume that service.

This section assumes you have created and linked at least two sites.

<a id="system-creating-connector-yaml"></a>
## Creating a connector using YAML
<!--PROCEDURE-->

A connector binds a local workload to listeners in remote sites.
Listeners and connectors are matched using routing keys.

For more information about connectors see [Connector concept][connector].
For configuration details, see [Connector resource][connector-resource].

**Procedure**

1. Create a workload that you want to expose on the network, for example:
   ```bash
   kubectl create deployment backend --image quay.io/skupper/hello-world-backend --replicas 3
   ```

2. Create a connector resource YAML file:
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: Connector
   metadata:
     name: backend
     namespace: east
   spec:
     routingKey: backend
     selector: app=backend
     port: 8080
   ```
   This creates a connector in the `east` site and exposes the `backend` deployment on the network on port 8080.
   You can create a listener on a different site using the matching routing key `backend` to address this service.

   To create the connector resource:

   ```bash
   skupper system apply -f <filename>
   ```

   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

3. Check the connector status:
   ```bash
   skupper connector status
   ```
   
   For example:
   
   ```text
   NAME    STATUS  ROUTING-KEY     SELECTOR        HOST    PORT    HAS MATCHING LISTENER    MESSAGE
   backend Pending backend         app=backend             8080    false   No matching listeners
   ```
   **📌 NOTE**
   By default, the routing key name is set to the name of the connector.
   If you want to use a custom routing key, set `spec.routingKey` to your custom value.

<a id="system-creating-listener-yaml"></a>
## Creating a listener using YAML
<!--PROCEDURE-->

A listener binds a local connection endpoint to connectors in remote sites. 
Listeners and connectors are matched using routing keys.

For more information about listeners, see [Listener concept][listener].
For configuration details, see [Listener resource][listener-resource].

**Procedure**

1. Identify a connector that you want to use.
   Note the routing key of that connector.

2. Create a listener resource YAML file:
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: Listener
   metadata:
     name: backend
     namespace: west
   spec:
     routingKey: backend
     host: east-backend
     port: 8080
   ```
   This creates a listener on the local system site and matches it with connectors that use the routing key `backend`.
   The listener accepts connections on port 8080 using the configured host value.

   To create the listener resource:

   ```bash
   skupper system apply -f <filename>
   ```

   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

3. Check the listener status:
   ```bash
   skupper listener status
   ```
   
   For example:
   
   ```text
   NAME      STATUS  ROUTING-KEY  HOST     PORT  MATCHING-CONNECTOR  MESSAGE
   backend   Ready   backend      0.0.0.0  8080  true                OK
   ```
   
   **📌 NOTE**
   There must be a `MATCHING-CONNECTOR` for the service to operate.

[connector]: https://skupperproject.github.io/refdog/concepts/connector.html
[listener]: https://skupperproject.github.io/refdog/concepts/listener.html
[connector-resource]: https://skupperproject.github.io/refdog/resources/connector.html
[listener-resource]: https://skupperproject.github.io/refdog/resources/listener.html
