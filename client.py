#!/usr/bin/env python3
"""
Simple client to exercise the ACP Ping RPC with plain text payload.
"""
import grpc
import acp_pb2
import acp_pb2_grpc

def run_ping():
    channel = grpc.insecure_channel("localhost:50051")
    stub = acp_pb2_grpc.ACPServiceStub(channel)
    msg = acp_pb2.AgentMessage(
        agent_id="WeThinG::Tester",
        content_type="text/plain",
        payload=b"PING"
    )
    resp = stub.Ping(msg)
    print(f"Received Pong -> agent_id={resp.agent_id}, payload={resp.payload}")

if __name__ == "__main__":
    run_ping()