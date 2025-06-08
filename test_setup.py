#!/usr/bin/env python3
"""
Quick test script to verify ACP server setup
"""
import sys
import subprocess
import time
import signal
import os

def test_imports():
    """Test if protobuf files can be imported"""
    try:
        import acp_pb2
        import acp_pb2_grpc
        print("✅ Protobuf imports working")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Run: python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. acp.proto")
        return False

def test_server_client():
    """Test server and client communication"""
    print("🚀 Testing server/client communication...")
    
    # Start server in background
    server_process = subprocess.Popen([sys.executable, "server.py"], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
    
    # Give server time to start
    time.sleep(2)
    
    try:
        # Test basic client
        result = subprocess.run([sys.executable, "client.py"], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ Basic client test passed")
            print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ Basic client test failed: {result.stderr}")
            return False
            
        # Test genesis client
        result = subprocess.run([sys.executable, "client_genesis.py"], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ Genesis client test passed")
            print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ Genesis client test failed: {result.stderr}")
            return False
            
        return True
        
    finally:
        # Clean up server process
        server_process.terminate()
        try:
            server_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            server_process.kill()

def main():
    print("🔧 ACP Server Test Suite")
    print("=" * 30)
    
    # Check if we're in virtual environment
    if not os.path.exists("venv/bin/activate"):
        print("❌ Virtual environment not found")
        print("Run: python3 -m venv venv && source venv/bin/activate")
        return False
        
    # Test imports
    if not test_imports():
        return False
        
    # Test server/client
    if not test_server_client():
        return False
        
    print("\n🎉 All tests passed! ACP server is ready to use.")
    print("\nTo start server: source venv/bin/activate && python server.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
