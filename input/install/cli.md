<a id="installing-cli"></a>
# Install the Skupper CLI
<!--PROCEDURE-->


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
