<a id="kube-exposing-services-yaml"></a>
# Exposing services on the application network using YAML
<!--ASSEMBLY-->

After creating an application network by linking sites, you can expose services from one site using connectors and consume those services on other sites using listeners.

A *routing key* is a string that matches one or more connectors with one or more listeners.
For example, if you create a connector with the routing key `backend`, you need to create a listener with the routing key `backend` to consume that service.

This section assumes you have created and linked at least two sites.

<!-- Creating a connector on Kubernetes using YAML -->
<a id="kube-creating-connector-yaml"></a>
## Creating a connector using YAML
<!--PROCEDURE-->

A connector binds a local workload to listeners in remote sites.
Listeners and connectors are matched using routing keys.

There are many options to consider when creating connectors using YAML, see [Connector resource][connector-resource].

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
   kubectl apply -f <filename>
   ```

   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

3. Check the connector status:
   ```bash
   kubectl get connector
   ```
   
   For example:
   
   ```
   NAME    STATUS  ROUTING-KEY     SELECTOR        HOST    PORT    HAS MATCHING LISTENER    MESSAGE
   backend Pending backend         app=backend             8080    false   No matching listeners
   ```
   **📌 NOTE**
   By default, the routing key name is set to the name of the connector.
   If you want to use a custom routing key, set `spec.routingKey` to your custom value.

<!-- Creating a listener on Kubernetes using YAML -->
<a id="kube-creating-listener-yaml"></a>
## Creating a listener using YAML
<!--PROCEDURE-->

A listener binds a local connection endpoint to connectors in remote sites. 
Listeners and connectors are matched using routing keys.

For more information about listeners. see [Listener concept][listener].

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
   This creates a listener in the `west` site and matches with the connector that uses the routing key `backend`. 
   It also creates a service named  `east-backend` exposed on port 8080 in the current namespace.

   To create the listener resource:

   ```bash
   kubectl apply -f <filename>
   ```

   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

3. Check the listener status:
   ```bash
   kubectl get listener
   ```
   
   For example:
   
   ```
   NAME      ROUTING KEY   PORT   HOST           STATUS   HAS MATCHING CONNECTOR   MESSAGE
   backend   backend       8080   east-backend   Ready    true                     OK   
   ```
   
   **📌 NOTE**
   There must be a `MATCHING-CONNECTOR` for the service to operate.

<a id="kube-creating-multikeylistener-yaml"></a>
## Creating a multi-key listener using YAML
<!--PROCEDURE-->

A multi-key listener binds a single local host and port to multiple routing keys in remote sites.
Use a multi-key listener when you want one service endpoint to aggregate traffic from multiple connectors.

With multi-key listeners, you must choose a strategy which determines how the traffic is distributed:

* priority - Uses the first routing key in list that is available for traffic. If the connector becomes unavailable, the listener matches with the next available routing key in list.
* weighted - Uses the routing keys in proportion to the assigned weights. For example, if `backend1` is assigned 25 and `backend2` is assigned 75, then only a quarter of the TCP connections are directed to `backend1`.

Multi-key listeners provide predictable traffic distribution from the client side and are **not influenced by link costs**.

For configuration details, see [MultiKeyListener resource][multikeylistener-resource].

**Prerequisites**

* Multiple connectors created with different routing keys. See [Creating a connector using YAML](#kube-creating-connector-yaml).

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
   kubectl apply -f <filename>
   ```

   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

4. Check the multi-key listener status:
   ```bash
   kubectl get multikeylistener
   ```

   **📌 NOTE**
   If you need to change strategy after you created a multi-key listener, you must delete and recreate the resource. This does not affect changing routing keys or weights.

<a id="kube-creating-attachedconnector-yaml"></a>
## Creating a connector for a different namespace using YAML
<!--PROCEDURE-->

A connector binds a local workload to listeners in remote sites.

If you create a site in one namespace and need to expose a service in a different namespace, use this procedure to create an *attached connector* in the other namespace and an *AttachedConnectorBinding* in the site namespace.

* An attached connector is a connector in a peer namespace, that is, not the site namespace.
* The AttachedConnectorBinding is a binding to an attached connector in a peer namespace and is created in the site namespace.
* Creating attached connectors requires that Skupper is deployed cluster wide.

For configuration details, see [Connector resource][connector-resource].

**Procedure**

1. Create a workload that you want to expose on the network in a non-site namespace, for example:
   ```bash
   kubectl create deployment backend --image quay.io/skupper/hello-world-backend --replicas 3 --namespace attached
   ```

2. Create an AttachedConnector resource YAML file in the same namespace:
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: AttachedConnector
   metadata:
     name: backend
     namespace: attached
   spec:
     siteNamespace: skupper
     selector: app=backend
     port: 8080
   ```

   To create the AttachedConnector resource:

   ```bash
   kubectl apply -f <filename>
   ```

   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

3. Create an AttachedConnectorBinding resource YAML file in the site namespace:
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: AttachedConnectorBinding
   metadata:
     name: backend            
     namespace: east            
   spec:
     connectorNamespace: attached
     routingKey: backend
   ```

   To create the AttachedConnectorBinding resource:

   ```bash
   kubectl apply -f <filename>
   ```

   where `<filename>` is the name of a YAML file that is saved on your local filesystem.



4. Check the AttachedConnectorBinding status from the context of the site namespace:
   ```bash
   kubectl get AttachedConnectorBinding
   ```
   
   For example:
   
   ```
   NAME      ROUTING KEY   CONNECTOR NAMESPACE   STATUS   HAS MATCHING LISTENER
   backend   backend       attached              Ready    true
   ```

[connector]: https://skupperproject.github.io/refdog/concepts/connector.html
[listener]: https://skupperproject.github.io/refdog/concepts/listener.html

[connector-resource]: https://skupperproject.github.io/refdog/resources/connector.html
[listener-resource]: https://skupperproject.github.io/refdog/resources/listener.html
[multikeylistener-resource]: https://skupperproject.github.io/refdog/resources/multi-key-listener.html
