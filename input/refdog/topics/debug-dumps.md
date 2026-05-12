---
render_macros: false
---

# Debug dumps

- The purpose of a debug dump is to package up the details of a site
  so another party can identify and fix a problem.
- A dump is a tarball containing various files with the site details.
- Key elements include site resources and status; component versions,
  config files, and logs; and info about the environment where Skupper
  is running.
- Should we include workloads in the namespace?  Services, deployments, pods?
- .txt file summaries for some things?
- What details about the overall network should we get?
  - Links from other sites?

~~~
# Same as the output of 'skupper version -o yaml'
version.yaml

# Same as the output of 'kubectl -n <site-namespace> get <kind>/<name> -o yaml'
resources/<kind>-<name>.yaml

# Same as the output of 'kubectl -n <skupper-namespace> get <kind>/<name> -o yaml'
resources/<kind>-<name>.yaml
~~~

<!-- components/controller/pods/<name>/log.txt -->
<!-- components/controller/pods/<name>/log.txt -->
<!-- components/router/log.txt -->

<!-- platform.yaml  # Info about the platform and namespace hosting the site -->

<!-- components/ -->
<!--   controller/ -->
<!--     <config file> -->
<!--     controller.log -->
<!--   router/ -->
<!--     <config file> -->
<!--     router.log -->
<!--     kube-adaptor.log -->
<!--   network-observer/ -->
<!--     <config file> -->
<!--     network-observer.log -->
