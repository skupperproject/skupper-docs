<a id="kube-installing-controller"></a>
# Installing the Skupper controller

If you are using Skupper on local systems (Podman, Docker, Linux), you must [install the CLI](#installing-cli).

Before you can create a site on Kubernetes, you must install the Skupper controller. 
You can install the controller using the following methods:

* Directly using YAML
* Helm charts
* Operator 

After installing the Skupper controller, you can create sites using the CLI or YAML:

* [Creating a site using the CLI][cli-site]
* [Creating a site using YAML][yaml-site]

[cli-site]: ../kube-cli/site-configuration.html
[yaml-site]: ../kube-yaml/site-configuration.html

**NOTE**: If you install the controller scoped to cluster, you can create sites in any namespace.
If you scope the controller to a namespace, you can only create sites in that namespace.


<a id="kube-installing-controller-yaml"></a>
## Installing the Skupper controller using YAML

**Prerequisites**

* cluster-admin access to cluster

**Procedure**

Install a cluster-scoped controller using the following commands:

```bash
kubectl apply -f https://github.com/skupperproject/skupper/releases/download/{{skupper_cli_version}}/skupper-cluster-scope.yaml
```

Install a namespace-scoped controller using the following commands:

```bash
kubectl apply -f https://github.com/skupperproject/skupper/releases/download/{{skupper_cli_version}}/skupper-namespace-scope.yaml
```



<a id="kube-installing-controller-helm"></a>
## Installing the Skupper controller using the Skupper Helm charts

**Prerequisites**

* cluster-admin access to cluster
* helm (See https://helm.sh/docs/intro/install/)


**Procedure**

Run the following command to install a cluster-scoped controller:

```
helm install skupper oci://quay.io/skupper/helm/skupper --version {{skupper_cli_version}}
```
To install a namespace-scoped controller, add the `--set scope=namespace` option.


<!--
<a id="kube-installing-controller-operator"></a>
## Installing the Skupper controller using the Skupper Operator

**Prerequisites**

* cluster-admin access to cluster
* OpenShift

**Procedure**

1. Navigate to the **OperatorHub** in the **Administrator** view.
2. Search for `Skupper`, provided by `Skupper project`.
3. Select **stable-2.0** from **Channel**.
4. Select the latest **Version**.
5. Click **Install**.
-->

<a id="installing-cli"></a>
## Installing the Skupper CLI


You can use the Skupper CLI with Kubernetes or on local systems (Podman, Docker, Linux). 

On local systems, the CLI is all you require to create a site.

**Procedure**

To download the latest release:

```bash
curl https://skupper.io/v2/install.sh | sh
```

To download a specific version, download from [Releases](https://github.com/skupperproject/skupper/releases) page.


On local systems, you can install the controller using:

```bash
skupper system install -p  [podman, docker, linux]
```

## Upgrading sites

To upgrade a site, you need to upgrade the controller using the same method you used to install Skupper, for example, one of the following:

* Applying the latest Helm chart
* Applying the latest YAML

To update the Skupper CLI:

```bash
curl https://skupper.io/v2/install.sh | sh
```


### Upgrading local sites

There are two distinct procedures for updating your Skupper installation: updating the site configuration and manually updating the controller.

**Standard Site Update** 

To update an existing site to the latest images or configuration matching your current CLI version:

**Procedure**

1. Ensure you have the latest version of the Skupper CLI installed.
2. Run the reload command:
	```shell
	skupper system reload
	```
	*This command refreshes the site definition and pulls the latest images associated with the CLI version.*

**Updating the controller** 

Currently, `skupper system uninstall` protects active sites by refusing to run if a site is detected. However, if you need to force an update to the **controller** itself (to pick up a new controller version) without deleting your sites, follow this manual workaround:

**Prerequisites** 

* Ensure your CLI is updated to the target version.

**Procedure**

1. Stop and remove the controller container. The container is named `<user>-skupper-controller`.
	
    **Podman**
    ```
	podman rm -f <user>-skupper-controller
	```
    **Docker**
    ```
	docker rm -f <user>-skupper-controller
	```
	*Note: Replace `<user>` with the specific username under which Skupper is running.*

2. Re-install the controller.
    Run the install command to recreate the controller using the new CLI version.
	```
	skupper system install
	```

3. Verify the controller is recreated with the updated version.
