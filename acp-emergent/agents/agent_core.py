class AgentCore:
    """Minimal agent core demonstrating basic step behavior."""

    def __init__(self, name: str = "agent"):
        self.name = name

    def step(self) -> None:
        """Execute a single agent step."""
        print(f"{self.name} executing step")
