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

<a id="system-creating-multikeylistener-yaml"></a>
## Creating a multi-key listener using YAML
<!--PROCEDURE-->

A multi-key listener binds a single local host and port to multiple routing keys in remote sites.
Use a multi-key listener when you want one service endpoint to aggregate traffic from multiple connectors.

With multi-key listeners, you must choose a strategy which determines how the traffic is distributed:

* priority - Uses the first routing key in list that is available for traffic. If the connector becomes unavailable, the listener matches with the next available routing key in list.
* weighted - Uses the routing keys in proportion to the assigned weights. For example, if `backend1` is assigned 25 and `backend2` is assigned 75, then only a quarter of the TCP connections are directed to `backend1`.

Multi-key listeners provide predictable traffic distribution from the client side and typically are not influenced by link costs.

For configuration details, see [Listener resource][listener-resource].

**Prerequisites**

* Multiple connectors created with different routing keys. See [Creating a connector using YAML](#system-creating-connector-yaml).

**Procedure**

1. Identify the connectors that you want to aggregate.
   Note the routing keys for each connector.

2. Determine which strategy is best for your use case. For example, failover is best achieved using the `priority` strategy.


3. Create a multi-key listener resource YAML file.
   For example:
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: MultiKeyListener
   metadata:
     name: mkl-backend
   spec:
     host: mkl-backend
     port: 9092
     strategy:
       weighted:
         routingKeys:
           east-backend: 1
           west-backend: 1
   ```
   This creates a listener named `mkl-backend` that exposes a single endpoint on port 9092 and distributes traffic evenly across the `east-backend` and `west-backend` routing keys.

   To prefer one routing key first and fall back to another, use the `priority` strategy:
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: MultiKeyListener
   metadata:
     name: mkl-backend-priority
   spec:
     host: mkl-backend-priority
     port: 9095
     strategy:
       priority:
         routingKeys:
           - east-backend-http
           - west-backend-http
   ```

   To create the multi-key listener resource:

   ```bash
   skupper system apply -f <filename>
   ```

   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

   ```

   **📌 NOTE**
   If you need to change strategy after you created a multi-key listener, you must delete and recreate the resource. This does not affect changing routing keys or weights.

[connector]: https://skupperproject.github.io/refdog/concepts/connector.html
[listener]: https://skupperproject.github.io/refdog/concepts/listener.html
[connector-resource]: https://skupperproject.github.io/refdog/resources/connector.html
[listener-resource]: https://skupperproject.github.io/refdog/resources/listener.html
