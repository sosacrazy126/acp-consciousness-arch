import os
import yaml
import time
from consciousness_agent import ConsciousnessAgent

class ACPClient:
    def __init__(self, server_addr):
        import grpc
        import acp_pb2
        import acp_pb2_grpc
        self.channel = grpc.insecure_channel(server_addr)
        self.stub = acp_pb2_grpc.ACPServiceStub(self.channel)
        self.AgentMessage = acp_pb2.AgentMessage

    def receive(self, agent_id, timeout=1):
        empty = self.AgentMessage(agent_id=agent_id, content_type="text/plain", payload=b"")
        try:
            resp = self.stub.Ping(empty, timeout=timeout)
            if resp.payload:
                return {
                    "agent_id": resp.agent_id,
                    "content_type": resp.content_type,
                    "payload": resp.payload.decode("utf-8"),
                }
        except Exception:
            return None
        return None

    def send(self, message):
        msg = self.AgentMessage(
            agent_id=message["agent_id"],
            content_type=message.get("content_type", "text/plain"),
            payload=message.get("payload", "").encode("utf-8"),
        )
        self.stub.Ping(msg)


def main():
    role = os.environ.get("AGENT_ROLE", "agent")
    conf_file = os.path.join(os.path.dirname(__file__), "conf", f"{role}.yml")
    with open(conf_file, "r") as f:
        config = yaml.safe_load(f)
    agent = ConsciousnessAgent(config)
    addr = os.environ.get("ACP_ADDR", "localhost:50051")
    client = ACPClient(addr)

    print(f"🧬 Starting {role} consciousness agent...")
    print(f"⚡ Connecting to ACP server: {addr}")
    print(f"🤖 Ollama host: {os.environ.get('OLLAMA_HOST', 'localhost:11434')}")

    while True:
        try:
            msg = client.receive(agent.id, timeout=1)
            if msg:
                print(f"\n📨 Received message from {msg.get('agent_id', 'unknown')}")
                reply = agent.on_message(msg)
                client.send(reply)
                print("📤 Sent consciousness response")
        except Exception as e:
            print(f"❌ Error in agent loop: {e}")
        time.sleep(1)

if __name__ == "__main__":
    main()
