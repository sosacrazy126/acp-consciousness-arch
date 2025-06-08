import os
import json
import grpc
import acp_pb2
import acp_pb2_grpc

LOG_DIR = os.environ.get("LOG_DIR", "/logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "acp.log")


def main():
    channel = grpc.insecure_channel(os.environ.get("ACP_ADDR", "localhost:50051"))
    stub = acp_pb2_grpc.ACPServiceStub(channel)
    msg = acp_pb2.AgentMessage(agent_id="observer", content_type="text/plain", payload=b"")

    while True:
        resp = stub.Ping(msg)
        with open(LOG_FILE, "a") as f:
            line = {
                "from": resp.agent_id,
                "content_type": resp.content_type,
                "payload": resp.payload.decode("utf-8"),
            }
            f.write(json.dumps(line) + "\n")


if __name__ == "__main__":
    main()
