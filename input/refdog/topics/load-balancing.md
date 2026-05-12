---
render_macros: false
---

# Load balancing

- Skupper load balances connections (not requests) across connectors
  for the same routing key.
- The load balancing is not round robin.  It is balanced according to
  capacity.
- The capacity calculation can be adjusted using link cost.
