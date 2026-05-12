---
render_macros: false
---

# Site linking

- Using tokens and the CLI
- Using tokens and YAML
- Token distribution methods
- Using link generation
- Using a network-scoped CA
- Special concerns for non-Kube sites

## Using kubectl to generate an access token from an access grant

~~~ sh
kubectl -n sk1 get accessgrant/<grant-name> -o template --template '
apiVersion: skupper.io/v2alpha1
kind: AccessToken
metadata:
  name: <token-name>
spec:
  code: "{{{ .status.code }}}"
  ca: {{{ printf "%q" .status.ca }}}
  url: "{{{ .status.url }}}"
' > token.yaml
~~~
