# Linking sites on Kubernetes using the Skupper CLI

Using the skupper command-line interface (CLI) allows you to create links between sites.

.Prequisites

* Two sites
* At least one site with `enable-link-access` enabled.

**📌 NOTE**
Traffic load is based on the number of concurrent TCP connections, so 'round robin' behavior should not be expected.
