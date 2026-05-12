<a id="system-exposing-services-cli"></a>
# Exposing services on the application network using the CLI
<!--ASSEMBLY-->

Use the CLI on local systems to create connectors and listeners for services on the application network.

After creating an application network by linking sites, you can expose services from one site using connectors and consume those services on other sites using listeners.
A *routing key* is a string that matches one or more connectors with one or more listeners.
For example, if you create a connector with the routing key `backend`, you need to create a listener with the routing key `backend` to consume that service.

This section assumes you have created and linked at least two sites.

<a id="system-creating-connector-cli"></a>
## Creating a connector using the CLI
<!--PROCEDURE-->

A connector binds a local workload to listeners in remote sites.
Listeners and connectors are matched using routing keys.

For more information about connectors see [Connector concept][connector]

**Prerequisites**

* The `skupper` CLI is installed.
* The `SKUPPER_PLATFORM` environment variable is set to one of * `podman`,`docker` or `linux`.

There are many options to consider when creating connectors using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

**Procedure**

1. Create a server that you want to expose on the network.
   For example, run a HTTP server on port 8080.

2. Create a connector:
   ```bash
   skupper connector create <name> <port> [--routing-key <name>]
   ```
   For example:

   ```bash
   skupper connector create my-server 8080 --host localhost
   ```
3. Check the connector status:
   ```bash
   skupper connector status
   ```
   
   For example:
   
   ```text
   $ skupper connector status
   NAME		STATUS	ROUTING-KEY	HOST		PORT
   my-server	Ok	my-server	localhost	8081

   ```
   **📌 NOTE**
   By default, the routing key name is set to the name of the connector.
   If you want to use a custom routing key, set the `--routing-key` to your custom name.

   Apply the configuration using:
   ```bash
   skupper system reload
   ```

<a id="system-creating-listener-cli"></a>
## Creating a listener using the CLI
<!--PROCEDURE-->

A listener binds a local connection endpoint to connectors in remote sites. 
Listeners and connectors are matched using routing keys.

**Prerequisites**

* The `skupper` CLI is installed.
* The `SKUPPER_PLATFORM` environment variable is set to one of * `podman`,`docker` or `linux`.

There are many options to consider when creating listeners using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

**Procedure**

1. Identify a connector that you want to use.
   Note the routing key of that connector.

2. Create a listener:
   ```bash
   skupper listener create <name> <port> [--routing-key <name>]
   ```
   For example:
   ```text
   $ skupper listener create my-server 8080
   File written to /home/user/.local/share/skupper/namespaces/default/input/resources/Listener-my-server.yaml
   ```
   Apply the configuration using:
   ```bash
   skupper system reload
   ```



3. Check the listener status:
   ```bash
   skupper listener status
   ```
   
   For example:
   
   ```text
   $ skupper listener status
   NAME      STATUS  ROUTING-KEY  HOST     PORT  MATCHING-CONNECTOR  MESSAGE
   backend   Ready   backend      0.0.0.0  8080  true                OK

   ```
   
   **📌 NOTE**
   There must be a matching connector for the service to operate.
   By default, the routing key name is the listener name.
   If you want to use a custom routing key, set the `--routing-key` to your custom name.

[cli-ref]: https://skupperproject.github.io/refdog/commands/index.html
[connector]: https://skupperproject.github.io/refdog/concepts/connector.html
[listener]: https://skupperproject.github.io/refdog/concepts/listener.html
