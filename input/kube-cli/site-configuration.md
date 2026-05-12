<a id="kube-creating-site-cli"></a>
# Creating a site on Kubernetes using the Skupper CLI
<!--ASSEMBLY-->

Using the skupper command-line interface (CLI) allows you to create and manage sites from the context of the current namespace.

A typical workflow is to create a site, link sites together, and expose services to the application network.

<a id="kube-checking-cli"></a>
## Checking the Skupper CLI
<!--PROCEDURE-->

Installing the skupper command-line interface (CLI) provides a simple method to get started with Skupper.

**Procedure**

1. Follow the instructions for [Installing Skupper](https://skupper.io/releases/index.html).

2. Verify the installation.
   ```bash
   skupper version
   
   COMPONENT               VERSION
   cli                     {{skupper_cli_version}}
   ```

<a id="kube-creating-simple-site-cli"></a>
## Creating a simple site using the CLI on Kubernetes
<!--PROCEDURE-->

Use the Skupper CLI to create a site on Kubernetes from the current namespace context.

**Prerequisites**

* The `skupper` CLI is installed.
* The Skupper controller is running on the Kubernetes cluster.

**Procedure**

1. Check that the `SKUPPER_PLATFORM` environment is unset or set to `kubernetes`.

   * `kubernetes` - default
   * `podman`
   * `docker`
   * `linux`

2. Create a site on Kubernetes:

   ```bash
   skupper site create <site-name> --namespace <namespace>
   ```
   Specifying the namespace is not required if the context is set to the namespace where you want to create the site.
   For example:
   ```bash
   skupper site create my-site
   
   Waiting for status...
   Site "my-site" is ready.
   ```
There are many options to consider when creating sites using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

   For example, `--enable-link-access` allows you to create tokens and link *to* this site.
   By default, this option is disabled, but you can change the setting later:
   ```bash
   skupper site update --enable-link-access
   ```

   You can use `--timeout <time>` to specify the maximum time that the CLI waits for the site status to report `ready`.
   ```bash
   skupper site create my-site --timeout 2m
   ```
   The timeout option does not stop the site from being created, but if the site is not ready, the following is output:
   ```bash
   Site "my-site" is not yet ready: Pending
   ```
   You can check the status of the site at any time by using `skupper site status`.

   By default, the router CPU allocation is BestEffort as described in [Pod Quality of Service Classes](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/), and this might affect performance under network load.
   To configure site resources, see [Setting site resources](../kube-yaml/site-configuration.html#kube-site-resources-yaml).


<a id="kube-ha-cli"></a>
## Creating a high availability site using the CLI on Kubernetes
<!--PROCEDURE-->

Create a highly available Skupper site on Kubernetes by enabling HA mode in the CLI.

You can create a site that is highly available by using the `ha` option.
High availability mode is intended to maintain service continuity during router restarts or pod rescheduling, but it does not provide failover if network connectivity between sites is lost.
High availability mode deploys two router pods with anti-affinity rules to ensure service continuity during node failures.

**Prerequisites**

* The `skupper` CLI is installed.
* The Skupper controller is running on the Kubernetes cluster.

**Procedure**

1. Create a high availability site on Kubernetes:

   ```bash
   skupper site create <site-name> --enable-ha
   ```
   If the site already exists, you can use the `update` command to enable high availability:
   ```bash
   skupper site update --enable-ha
   ```
2. To verify that the site is running in high availability mode, run the following command:
   ```bash
   kubectl get site -o yaml | grep ha
   ```
   The output should be similar to the following:
   ```
   ha: true
   ```
   When high availability mode is enabled, two router pods are created so that traffic can continue if one pod restarts or is rescheduled.
   High availability can also help during a node failure.

<a id="kube-deleting-site-cli"></a>
## Deleting a site using the CLI on Kubernetes
<!--PROCEDURE-->

Delete a Skupper site on Kubernetes by using the CLI from the namespace where the site was created.

**Prerequisites**

* The `skupper` CLI is installed.

**Procedure**

1. Change context to the namespace where the site was created, for example:
   ```bash
   kubectl config set-context --current --namespace west
   ```

2. Enter the following command to delete a site:
   ```bash
   skupper site delete
   ```
[cli-ref]: https://skupperproject.github.io/refdog/commands/index.html
