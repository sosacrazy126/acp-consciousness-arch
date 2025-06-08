
# ACP Emergent Agent System

This directory contains a minimal scaffold for an emergent agent setup. The blueprint includes a simple agent core, a lightweight ACP server, and Docker configuration to run them together.

Use `docker compose up --build` to build and start the containers.

# ACP Emergent System

This directory contains a containerized setup for running multiple agents
communicating through the ACP gRPC server. Each agent loads its own
configuration and interacts with the server via polling.

## Usage

1. Build and start the network:

```bash
docker compose up --build
```

2. Observe logs in `./logs` after running.

The scenario `scenarios/genesis_open_conflict.json` can be submitted via a
client to kick off the negotiation.
