---
render_macros: false
---

# System TLS credentials

- Kubernetes already has secrets.  The Docker, Podman, and Linux
  platforms use a directory in a well-known location.
- Location: <namespace>/input/certs and <namespace>/input/issuers
- Also: <namespace>/runtime/certs and issuers
- Each directory has the files...
