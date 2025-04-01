<a id="system-yaml-service-exposure"></a>
# Exposing services on the application network using YAML

After creating an application network by linking sites, you can expose services from one site using connectors and consume those services on other sites using listeners.
A *routing key* is a string that matches one or more connectors with one or more listeners.
For example, if you create a connector with the routing key `backend`, you need to create a listener with the routing key `backend` to consume that service.

This section assumes you have created and linked at least two sites.

## Creating a connector using YAML

A connector binds a local workload to listeners in remote sites.
Listeners and connectors are matched using routing keys.

For more information about connectors see [Connector concept][connector]

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
   If you want to use a custom routing key, set the `--routing-key` to your custom name.

There are many options to consider when creating connectors using YAML, see [CLI Reference][cli-ref], including *frequently used* options.


## Creating a listener using YAML

A listener binds a local connection endpoint to connectors in remote sites. 
Listeners and connectors are matched using routing keys.

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

   To create the connector resource:

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

There are many options to consider when creating connectors using YAML, see [CLI Reference][cli-ref], including *frequently used* options.

[connector]: https://skupperproject.github.io/refdog/concepts/connector.html
[listener]: https://skupperproject.github.io/refdog/concepts/listener.html