# Using the Skupper Operator on Kubernetes

The Skupper operator creates and manages Skupper sites in Kubernetes.

You can install the Operator as described in [Installing the Operator using the CLI](#installing-the-operator-using-the-cli).
service network

<dl><dt><strong>📌 NOTE</strong></dt><dd>

Installing an Operator requires administrator-level privileges for your Kubernetes cluster.
</dd></dl>

After installing the Operator, you can create a site by deploying a ConfigMap as described in [Creating a site using the Skupper Operator](#creating-a-site-using-the-skupper-operator)

## Installing the Operator using the CLI

The steps in this section show how to use the `kubectl` command-line interface (CLI) to install and deploy the latest version of the Skupper operator in a given Kubernetes cluster.

* The Operator Lifecycle Manager is installed in the cluster.
For more information, see the [QuickStart](https://olm.operatorframework.io/docs/getting-started/).

1. Download the Skupper Operator example files, for example:

   ```
   $ wget https://github.com/skupperproject/skupper-operator/archive/refs/heads/main.zip
   ```
2. Create a `my-namespace` namespace.
NOTE: If you want to use a different namespace, you need to edit the referenced YAML files.
   1. Create a new namespace:

      ```bash
      $ kubectl create namespace my-namespace
      ```
   2. Switch context to the namespace:

      ```bash
      $ kubectl config set-context --current --namespace=my-namespace
      ```
3. Create a CatalogSource in the `openshift-marketplace` namespace:

   ```bash
   $ kubectl apply -f examples/k8s/00-cs.yaml
   ```
4. Verify the skupper-operator catalog pod is running before continuing:

   ```bash
   $ kubectl -n olm get pods | grep skupper-operator
   ```
5. Create an OperatorGroup in the `my-namespace` namespace:

   ```bash
   $ kubectl apply -f examples/k8s/10-og.yaml
   ```
6. Create a Subscription  in the `my-namespace` namespace:

   ```bash
   $ kubectl apply -f examples/k8s/20-sub.yaml
   ```
7. Verify that the Operator is running:

   ```bash
   $ kubectl get pods -n my-namespace

   NAME                                     READY   STATUS    RESTARTS   AGE
   skupper-site-controller-d7b57964-gxms6   1/1     Running   0          1m
   ```

   If the output does not report the pod is running, use the following command to determine the issue that prevented it from running:

   ```
   $ kubectl describe pod -l name=skupper-operator
   ```

## Creating a site using the Skupper Operator

1. Create a YAML file defining the ConfigMap of the site you want to create.

   For example, create `skupper-site.yaml` that provisions a site with a console:

   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: skupper-site
     namespace: my-namespace
   data:
     console: "true"
     flow-collector: "true"
     console-user: "admin"
     console-password: "changeme"

   ```

   **📌 NOTE**\
   The console is a preview feature and may change before becoming fully supported by [skupper.io](https://skupper.io).
   Currently, you must enable the console on the same site as you enable the flow collector. This requirement may change before the console is fully supported by [skupper.io](https://skupper.io).

   You can also create a site without a console:

   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: skupper-site
     namespace: my-namespace
   ```
2. Apply the YAML to create a ConfigMap named `skupper-site` in the namespace you want to use:

   ```bash
   $ kubectl apply -f skupper-site.yaml
   ```
3. Verify that the site is created by checking that the Skupper router and service controller pods are running:

   ```bash
   $ kubectl get pods

   NAME                                          READY   STATUS    RESTARTS   AGE
   skupper-router-8c6cc6d76-27562                1/1     Running   0          40s
   skupper-service-controller-57cdbb56c5-vc7s2   1/1     Running   0          34s
   ```

   **📌 NOTE**\
   If you deployed the Operator to a single namespace, an additional site controller pod is also running.
