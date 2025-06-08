class AgentCore:
    """Minimal agent core demonstrating basic step behavior."""

    def __init__(self, name: str = "agent"):
        self.name = name

    def step(self) -> None:
        """Execute a single agent step."""
        print(f"{self.name} executing step")
=======
import json
import time

class AgentCore:
    """Minimal agent core handling messages and actions."""

    def __init__(self, config):
        self.id = config.get("id")
        self.role = config.get("role")
        self.goals = config.get("goals", {})
        self.memory = []  # TODO: replace with persistent storage

    def on_message(self, msg):
        """Handle inbound message and decide on reply."""
        self.memory.append({
            "timestamp": time.time(),
            "from": msg.get("agent_id"),
            "content": msg.get("payload"),
        })
        return self.act(msg)

    def act(self, msg):
        """Simple heuristic action stub."""
        # This placeholder simply echoes the message back
        reply = {
            "agent_id": self.id,
            "content_type": msg.get("content_type", "text/plain"),
            "payload": msg.get("payload"),
        }
        return reply
