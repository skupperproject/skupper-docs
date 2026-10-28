---
skip: true
---
<a id="skupper-upgrading-sites"></a>
# Upgrade sites
<!--PROCEDURE-->

To upgrade a site, you need to upgrade the controller using the same method you used to install Skupper, for example, one of the following:

* Applying the latest Helm chart
* Applying the latest YAML

To update the Skupper CLI:

```bash
curl https://skupper.io/v2/install.sh | sh
```


<a id="skupper-upgrading-local-sites"></a>
### Upgrade local sites
<!--PROCEDURE-->

There are two distinct procedures for updating your Skupper installation: updating the site configuration and manually updating the controller.

**Standard Site Update** 

To update an existing site to the latest images or configuration matching your current CLI version:

**Procedure**

1. Ensure you have the latest version of the Skupper CLI installed.
2. Run the reload command:
	```bash
	skupper system reload
	```
	*This command refreshes the site definition and pulls the latest images associated with the CLI version.*

<a id="skupper-upgrading-local-controller"></a>
### Upgrade the Skupper controller
<!--PROCEDURE-->

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