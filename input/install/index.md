# Installing the Skupper controller

Before you can create a site on Kubernetes, you must install the Skupper controller. 
You can install the controller using the following methods:

* Directly using YAML
* Operator (requires OLM)
* Helm charts

## Installing the Skupper controller using YAML

Install the latest version using the following commands:

```
kubectl apply -f https://raw.githubusercontent.com/skupperproject/skupper/v2/config/crd/bases/skupper_access_grant_crd.yaml
kubectl apply -f https://raw.githubusercontent.com/skupperproject/skupper/v2/config/crd/bases/skupper_access_token_crd.yaml
kubectl apply -f https://raw.githubusercontent.com/skupperproject/skupper/v2/config/crd/bases/skupper_attached_connector_anchor_crd.yaml
kubectl apply -f https://raw.githubusercontent.com/skupperproject/skupper/v2/config/crd/bases/skupper_attached_connector_crd.yaml
kubectl apply -f https://raw.githubusercontent.com/skupperproject/skupper/v2/config/crd/bases/skupper_certificate_crd.yaml
kubectl apply -f https://raw.githubusercontent.com/skupperproject/skupper/v2/config/crd/bases/skupper_connector_crd.yaml
kubectl apply -f https://raw.githubusercontent.com/skupperproject/skupper/v2/config/crd/bases/skupper_link_crd.yaml
kubectl apply -f https://raw.githubusercontent.com/skupperproject/skupper/v2/config/crd/bases/skupper_listener_crd.yaml
kubectl apply -f https://raw.githubusercontent.com/skupperproject/skupper/v2/config/crd/bases/skupper_router_access_crd.yaml
kubectl apply -f https://raw.githubusercontent.com/skupperproject/skupper/v2/config/crd/bases/skupper_secured_access_crd.yaml
kubectl apply -f https://raw.githubusercontent.com/skupperproject/skupper/v2/config/crd/bases/skupper_site_crd.yaml
kubectl apply -f https://raw.githubusercontent.com/skupperproject/skupper/v2/cmd/controller/deploy_cluster_scope.yaml
```

<!-- >
## Installing the Skupper controller using the Skupper Operator

