# Configuring Skupper sites using YAML{skupper-declarative}

Using YAML files to configure Skupper allows you to use source control to track and manage Skupper network changes.

## Installing Skupper using YAML

Installing Skupper using YAML provides a declarative method to install Skupper.
You can store your YAML files in source control to track and manage Skupper network changes.

* Access to a Kubernetes cluster

1. Log into your cluster.
If you are deploying Skupper to be available for all namespaces, verify you have `cluster-admin` privileges.
2. Deploy the site controller:
   * To install Skupper into the current namespace deploy the site controller using the following YAML:

     ```bash
     kubectl apply -f deploy-watch-current-ns.yaml
     ```
     where the contents of `deploy-watch-current-ns.yaml` is specified in the [watch-current-reference](#watch-current-reference) appendix.
   * To install Skupper for all namespaces:

     1. Create a namespace named `skupper-site-controller`.
     2. Deploy the site controller using the following YAML:

        ```bash
        kubectl apply -f deploy-watch-all-ns.yaml
        ```
        where the contents of `deploy-watch-all-ns.yaml` is specified in the [watch-all-reference](#watch-all-reference) appendix.
3. Verify the installation.

   ```bash
   $ kubectl get pods
   NAME                                       READY   STATUS    RESTARTS   AGE
   skupper-site-controller-84694bdbb5-n8slb   1/1     Running   0          75s
   ```

[id="creating-using-yaml"] 
== Creating a Skupper site using YAML

Using YAML files to create Skupper sites allows you to use source control to track and manage Skupper network changes.

* Skupper is installed in the cluster or namespace you want to target.
* You are logged into the cluster.

1. Create a YAML file to define the site, for example, `my-site.yaml`:

   ```bash
   ```
   The YAML creates a site with a console and you can create tokens from this site.

   To create a site that has no ingress:

   ```
   ```

2. Apply the YAML file to your cluster:

   ```bash
   kubectl apply -f ~/my-site.yml
   ```

See the [site-config-reference](#site-config-reference) section for more reference.

[id="linking-sites-using-yaml"] 
== Linking sites using YAML

While it is not possible to declaratively link sites, you can create a token using YAML.
Only use this procedure to create links if the Skupper CLI is not available in your environment.

* Skupper is installed on the clusters you want to link.
* You are logged into the cluster.

1. Log into the cluster you want to link to and change context to the namespace where Skupper is installed.
This site must have `ingress` enabled.
2. Create a YAML file named `token-request.yml` to request a token:

   ```
   apiVersion: v1
   kind: Secret
   metadata:
     labels:
       skupper.io/type: connection-token-request
     annotations:
       skupper.io/cost: "2"
     name: secret-name
   ```
3. Apply the YAML to the namespace to create a secret.

   ```bash
   $ kubectl apply -f token-request.yml
   ```
4. Create the token YAML from the secret.

   ```bash
   $ kubectl get secret -o yaml secret-name | yq 'del(.metadata.namespace)' > ~/token.yaml
   ```
5. Log into the cluster you want to link from and change context to the namespace where Skupper is installed.
6. Apply the token YAML.

   ```bash
   $ kubectl apply -f token.yml
   ```
7. Verify the link, allowing some time for the process to complete.

   ```bash
   $ skupper link status --wait 60
   ```

Skupper recommends using the CLI to create links. 

A future release of Skupper will provide an alternative declarative method to create links.

[id="site-config-reference"] 
## Site ConfigMap YAML reference

Using YAML files to configure Skupper requires that you understand all the fields so that you provision the site you require.

The following YAML defines a Skupper site:
```yaml
apiVersion: v1
data:
  name: my-site
  console: "true"
  flow-collector: "true"
  console-authentication: internal
  console-user: "username"
  console-password: "password"
  cluster-local: "false"
  edge: "false"
  service-sync: "true"
  ingress: "none"
kind: ConfigMap
metadata:
  name: skupper-site
```

* **name**\
Specifies the site name.
* **console**\
Enables the skupper console, defaults to `false`.
NOTE: You must enable `console` and `flow-collector` for the console to function.
* **flow-collector**\
Enables the flow collector, defaults to `false`.
* **console-authentication**\
Specifies the skupper console authentication method. The options are `openshift`, `internal`, `unsecured`.
* **console-user**\
Username for the `internal` authentication option.
* **console-password**\
Password for the `internal` authentication option.
* **cluster-local**\
Only accept connections from within the local cluster, defaults to `false`.
* **edge**\
Specifies whether an edge site is created, defaults to `false`.
* **service-sync**\
Specifies whether the services are synchronized across the {service-network}, defaults to `true`.
* **ingress**\
Specifies whether the site supports ingress.
If you do not specify a value, the default ingress ('loadbalancer' on Kubernetes, 'route' on OpenShift) is enabled. 
This allows you to create tokens usable from remote sites.

**📌 NOTE**\
All ingress types are supported using the same parameters as the `skupper` CLI.

[id="watch-current-reference"] 
## YAML for watching current namespace

The following example deploys Skupper to watch the current namespace.

```
```

[id="watch-all-reference"] 
## YAML for watching all namespaces

The following example deploys Skupper to watch all namespaces.

```
```
