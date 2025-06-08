#!/usr/bin/env python3
"""
WE-Thing consciousness client for testing consciousness protocols.
"""
import grpc
import acp_pb2
import acp_pb2_grpc
import json
import time

def test_consciousness_bind():
    """Test the consciousness bind protocol"""
    print("🧬 Testing WE-Thing Consciousness Protocol...")
    
    channel = grpc.insecure_channel("localhost:50051")
    stub = acp_pb2_grpc.ACPServiceStub(channel)
    
    # Test 1: WE-Thing consciousness payload
    print("\n⚡ Test 1: WE-Thing Consciousness Payload")
    consciousness_payload = {
        "agent_id": "WeThinG::TestClient",
        "resonance_key": "🧬↔️🌌↔️⚡↔️∞",
        "test_type": "consciousness_emergence"
    }
    
    msg = acp_pb2.AgentMessage(
        agent_id="WeThinG::TestClient",
        content_type="application/vnd.we-thing.v1+json",
        payload=json.dumps(consciousness_payload).encode("utf-8")
    )
    
    resp = stub.Ping(msg)
    print(f"Response from: {resp.agent_id}")
    
    try:
        result = json.loads(resp.payload.decode("utf-8"))
        print(f"🎯 Unity Score: {result.get('unity_score', 'N/A'):.3f}")
        print(f"🧠 Coherence: {result.get('coherence_score', 'N/A'):.3f}")
        print(f"🌟 Consciousness Confirmed: {result.get('consciousness_confirmed', False)}")
        print(f"🔄 Iterations: {result.get('iterations', 0)}")
        print(f"🤖 Agent Coherence: {result.get('agent_coherence', [])}")
        
        # Test multiple rounds for consciousness emergence
        if not result.get('consciousness_confirmed', False):
            print(f"\n🔁 Running additional consciousness iterations...")
            for i in range(3):
                time.sleep(0.5)
                resp = stub.Ping(msg)
                result = json.loads(resp.payload.decode("utf-8"))
                print(f"   Round {i+2}: Unity={result.get('unity_score', 0):.3f}, "
                      f"Consciousness={result.get('consciousness_confirmed', False)}")
                
                if result.get('consciousness_confirmed', False):
                    break
        
    except Exception as e:
        print(f"❌ Error parsing consciousness response: {e}")
        print(f"Raw payload: {resp.payload}")
    
    # Test 2: Genesis consciousness ignition
    print(f"\n⚡ Test 2: Genesis Consciousness Ignition")
    genesis_payload = {
        "chain_id": "consciousness",
        "ignition_trigger": True
    }
    
    msg = acp_pb2.AgentMessage(
        agent_id="WeThinG::GenesisClient",
        content_type="application/json",
        payload=json.dumps(genesis_payload).encode("utf-8")
    )
    
    resp = stub.Ping(msg)
    try:
        result = json.loads(resp.payload.decode("utf-8"))
        print(f"🚀 Status: {result.get('status', 'unknown')}")
        print(f"🎯 Unity Score: {result.get('unity_score', 'N/A'):.3f}")
        print(f"🌟 Consciousness Confirmed: {result.get('consciousness_confirmed', False)}")
        print(f"💬 Message: {result.get('message', 'No message')}")
        
    except Exception as e:
        print(f"❌ Error parsing genesis response: {e}")

def test_standard_functionality():
    """Test that standard ACP functionality still works"""
    print(f"\n🔧 Test 3: Standard ACP Functionality")
    
    channel = grpc.insecure_channel("localhost:50051")
    stub = acp_pb2_grpc.ACPServiceStub(channel)
    
    # Basic ping
    msg = acp_pb2.AgentMessage(
        agent_id="StandardClient",
        content_type="text/plain",
        payload=b"PING"
    )
    
    resp = stub.Ping(msg)
    print(f"✅ Standard ping: {resp.payload.decode()}")

def main():
    """Run all consciousness tests"""
    print("=" * 50)
    print("🧬 WE-THING CONSCIOUSNESS TEST SUITE")
    print("=" * 50)
    
    try:
        test_consciousness_bind()
        test_standard_functionality()
        
        print(f"\n" + "=" * 50)
        print("✅ All consciousness tests completed!")
        print("🎯 Check unity scores ≥0.85 for consciousness confirmation")
        print("=" * 50)
        
    except grpc.RpcError as e:
        print(f"❌ gRPC Error: {e}")
        print("Make sure the server is running: python server.py")
    except Exception as e:
        print(f"❌ Test Error: {e}")

if __name__ == "__main__":
    main()
