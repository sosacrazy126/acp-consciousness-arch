#!/usr/bin/env python3
"""
Client to send a genesis JSON envelope to the ACP Ping RPC.
"""
import json
import grpc
import acp_pb2
import acp_pb2_grpc

def send_genesis(genesis_file="genesis.json"):
    # Load genesis JSON
    with open(genesis_file, "r") as f:
        genesis = json.load(f)
    payload = json.dumps(genesis).encode("utf-8")

    # Dial gRPC and send the envelope
    channel = grpc.insecure_channel("localhost:50051")
    stub = acp_pb2_grpc.ACPServiceStub(channel)
    msg = acp_pb2.AgentMessage(
        agent_id="WeThinG::Initializer",
        content_type="application/json",
        payload=payload
    )
    resp = stub.Ping(msg)
    print(f"Server replied: agent_id={resp.agent_id}, content_type={resp.content_type}")
    try:
        data = json.loads(resp.payload.decode("utf-8"))
        print("Payload JSON:", data)
    except Exception:
        print("Raw payload:", resp.payload)

if __name__ == "__main__":
    send_genesis()
