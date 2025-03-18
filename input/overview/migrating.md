<a id="migrating"></a>
# Migrating from Skupper v1

Skupper v1 sites are not compatible with Skupper v2 sites.
While there are plans to create migration tooling, currently, the only way migrate an application network is to create a new network.

Terminology changes:

* **service network**: Application network or just network
* **service sync**: Services are not automatically available on other sites. You must create a *connector* on the site with the server process and a *listener* on the site with the client process. Also you must match the connector and listener with a *routing key* to expose a service.
* **Skupper Custom Resources**: On non-Kubernetes sites, you can now define your network using YAML. The YAML format is similar to Kubernetes YAML.

<a id="migrating-sites"></a>
## Creating sites

Creating sites using CLI:

```v1
contextA> skupper init
```

```v2
contextA> skupper site create
```

The site does not accept links by default.
Use `--enable-link-access` to allow other sites link to the new site.

On Podman, the site definition is created in `~/.local/share/skupper` and you must enter `skupper system setup` to complete site creation.

<a id="migrating-links"></a>
## Linking sites



```v1
contextA> skupper token create ~/token.yaml
contextB> skupper link create ~/token.yaml
```

```v2
contextA> skupper token issue ~/token.yaml
contextA> skupper token redeem ~/token.yaml
```

<a id="migrating-services"></a>
## Exposing services

```v1
contextA> skupper expose deployment/backend --port 8080
```

```v2
contextA> skupper connector create backend 8080
contextB> skupper listener create backend 8080
```

The new *routing-key* option gives you more control over how services are defined, for example to expose the service as `backend2` in contextB:

```v2
contextB> skupper listener create backend2 8080 --routing-key backend
```
