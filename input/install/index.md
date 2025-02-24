# Installing the Skupper controller

Before you can create a site on Kubernetes, you must install the Skupper controller. 
You can install the controller using the following methods:

* Directly using YAML
* Helm charts
* Operator 

## Installing the Skupper controller using YAML

.Prerequisites

* cluster-admin access to cluster

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

## Installing the Skupper controller using the Skupper Helm charts

.Prerequisites

* cluster-admin access to cluster
* helm (See https://helm.sh/docs/intro/install/)

<!-- >
## Installing the Skupper controller using the Skupper Operator

