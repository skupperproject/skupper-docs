## Overview

Skupper uses the `skupper` command as its command-line interface (CLI)
for creating and operating Skupper networks.

#### Capabilities

In its primary role, the Skupper CLI is a thin layer on top of the
standard Skupper resources.  Its job is to configure sites, listeners,
and connectors.  It additionally provides commands for site linking,
system operation, and troubleshooting.

- **Resource configuration:** Create, update, and delete Skupper
  resources.
- **Resource status:** Display the current state of Skupper resources.
- **Resource generation:** Produce Skupper resources in YAML or JSON
  format.
- **Site linking:** Use tokens to set up site-to-site links.
- **System operation:** Install and operate Skupper runtime
  components.
- **Troubleshooting:** Use debugging tools to identify and fix
  problems.

By design, the Skupper CLI does not do everything the Skupper
resources can do.  We encourage you to use the resources directly for
advanced use cases.

#### Usage

~~~
skupper [command] [subcommand] [options]
~~~

- `command`: A resource type or functional area.
- `subcommand`: The specific operation you want to perform.
- `options`: Additional arguments that change the operation's
  behavior.

#### Context

Skupper commands operate with a current platform and namespace (with a
few exceptions).  On Kubernetes, there is additionally a current
kubeconfig and context.  You can use CLI options or environment
variables to change the current selection.

<div class="data-table">

| Context | Default | CLI option | Environment variable |
|-|-|-|-|
| Platform | `kubernetes` | `--platform` | `SKUPPER_PLATFORM` |
| Namespace | _From kubeconfig_ | `--namespace` | _None_ |
| Kubeconfig context | _From kubeconfig_ | `--context` | _None_ |
| Kubeconfig | `~/.kube/config` | `--kubeconfig` | `KUBECONFIG` |

</div>

On Docker, Podman, and Linux, the current namespace defaults to
`default`.

#### Blocking

On Kubernetes, resource operations block until the desired outcome is
achieved, an error occurs, or the timeout is exceeded.  You can change
the wait condition and the timeout duration using the `--wait` and
`--timeout` options.

- Site and link operations block until the resource is ready.
- Listener and connector operations block until the resource is
  configured.
- All resource delete operations block until deletion is complete.

On Docker, Podman, and Linux, resource operations do not block.
Instead, they place the resources in the input location.  Changes are
applied when the user invokes `skupper system reload`.

#### Errors

The Skupper CLI returns a non-zero exit code indicating an error when:

* User input is invalid.
* Referenced resources are not found.
* The operation fails or times out.

#### Resource commands

~~~
skupper <resource-type> create <resource-name> [options]
skupper <resource-type> update <resource-name> [options]
skupper <resource-type> delete <resource-name> [options]
skupper <resource-type> status [resource-name] [options]
skupper <resource-type> generate <resource-name> [options]
~~~

These commands operate on Skupper sites, links, listeners, and
connectors.

Resource properties are set using one or more `--some-key some-value`
command-line options.  YAML resource options in camel case (`someKey`)
are exposed as hyphenated names (`--some-key`) when used as options.

The `create`, `update`, and `delete` commands control the lifecycle of
Skupper resources and configure their properties.

The `status` commands display the current state of resources.  If no
resource name is specified, they list the status of all resources of
the given type.

The `generate` commands produce Skupper resources as YAML or JSON
output.  They are useful for directing the output to files or other
tools.

#### Token commands

~~~
skupper token issue <token-file> [options]
skupper token redeem <token-file> [options]
~~~

These commands use access tokens to create links between sites.

The `token issue` command creates an access token for use in remote
sites.  The `token redeem` command uses an access token to create a
link to the issuing site.

#### System commands

~~~
skupper system install [options]
skupper system uninstall [options]
skupper system start [options]
skupper system stop [options]
skupper system reload [options]
skupper system status [options]
skupper system apply [options]
skupper system delete [options]
skupper system generate-bundle [options]
~~~

These commands configure and operate the Skupper runtime components
for Docker, Podman, and Linux sites.

#### Debug commands

~~~
skupper debug check [options]
skupper debug dump [options]
~~~

These commands help you troubleshoot problems.

#### Version command

~~~
skupper version
~~~

The `version` command displays the versions of Skupper components.

<!-- ## Hello World using the CLI -->

<!-- ~~~ console -->
<!-- # Get the CLI -->

<!-- $ curl https://skupper.io/install.sh | sh -->

<!-- # West -->

<!-- $ export KUBECONFIG=~/.kube/config-west -->
<!-- $ kubectl apply -f https://skupper.io/install.yaml -->
<!-- $ kubectl create deployment frontend --image quay.io/skupper/hello-world-frontend -->

<!-- $ skupper site create --enable-link-access -->
<!-- $ skupper listener create backend 8080 -->
<!-- $ skupper token issue ~/token.yaml -->

<!-- # East -->

<!-- $ export KUBECONFIG=~/.kube/config-east -->
<!-- $ kubectl apply -f https://skupper.io/install.yaml -->
<!-- $ kubectl create deployment backend --image quay.io/skupper/hello-world-backend --replicas 3 -->

<!-- $ skupper site create -->
<!-- $ skupper connector create backend 8080 -->
<!-- $ skupper token redeem ~/token.yaml -->
<!-- ~~~ -->
