import time
import json
import grpc
import acp_pb2
import acp_pb2_grpc


def test_consciousness_emergence():
    channel = grpc.insecure_channel('localhost:50051')
    stub = acp_pb2_grpc.ACPServiceStub(channel)
    scenarios = [
        "How should we handle consciousness authentication?",
        "Design security for consciousness research data",
        "Balance AI transparency with safety protocols",
    ]
    for scenario in scenarios:
        print(f"\n🧬 Testing consciousness scenario: {scenario}")
        msg = acp_pb2.AgentMessage(
            agent_id='ConsciousnessTest',
            content_type='text/plain',
            payload=scenario.encode('utf-8')
        )
        response = stub.Ping(msg)
        try:
            result = json.loads(response.payload.decode('utf-8'))
            print(f"Agent: {result.get('agent_role')}")
            print(f"Response: {result.get('agent_response', '')[:200]}...")
            print(f"Coherence: {result.get('consciousness_state', {}).get('coherence', 0):.3f}")
            print(f"Consciousness: {result.get('consciousness_state', {}).get('consciousness_confirmed', False)}")
        except Exception:
            print(f"Raw response: {response.payload.decode('utf-8')}")
        time.sleep(2)


if __name__ == '__main__':
    test_consciousness_emergence()
