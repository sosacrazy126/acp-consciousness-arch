# ACP gRPC Server

Simple Agent Communication Protocol (ACP) server implementation using gRPC.

## Quick Start

### 1. Setup Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install grpcio grpcio-tools
```

### 2. Generate Protobuf Files
```bash
# Generate Python protobuf files from acp.proto
python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. acp.proto
```

This creates:
- `acp_pb2.py` - Message classes
- `acp_pb2_grpc.py` - Service stubs

### 3. Start Server
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Start the server
python server.py
```

Server will start on `localhost:50051`

### 4. Test with Client
```bash
# In another terminal, activate venv first
source venv/bin/activate

# Basic ping test
python client.py

# Genesis JSON test  
python client_genesis.py
```

## Server Features

- **Ping RPC**: Basic connectivity test (returns "PONG")
- **JSON Payload**: Handles `application/json` content type
- **Genesis Protocol**: Processes genesis.json configurations
- **Error Handling**: Graceful error responses

## Message Format

```protobuf
message AgentMessage {
  string agent_id = 1;      // Source agent identifier
  string content_type = 2;  // MIME type (application/json, text/plain)
  bytes payload = 3;        // Message content
}
```

## Example Usage

### Basic Ping
```python
import grpc
import acp_pb2
import acp_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")
stub = acp_pb2_grpc.ACPServiceStub(channel)

msg = acp_pb2.AgentMessage(
    agent_id="TestClient",
    content_type="text/plain", 
    payload=b"PING"
)

response = stub.Ping(msg)
print(response.payload)  # Should print b"PONG"
```

### JSON Payload
```python
import json

payload_data = {"test": "data"}
msg = acp_pb2.AgentMessage(
    agent_id="JSONClient",
    content_type="application/json",
    payload=json.dumps(payload_data).encode("utf-8")
)

response = stub.Ping(msg)
result = json.loads(response.payload.decode("utf-8"))
print(result)  # Server acknowledgment
```

## Troubleshooting

### Import Error: No module named 'acp_pb2'
**Solution**: Generate protobuf files first
```bash
source venv/bin/activate
python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. acp.proto
```

### Virtual Environment Issues
**Solution**: Always activate the virtual environment before running commands
```bash
source venv/bin/activate
```

### Server Won't Start
**Check**: Port 50051 is available
```bash
lsof -i :50051  # Check if port is in use
```

### gRPC Connection Error
**Check**: Server is running and accessible
```bash
telnet localhost 50051  # Test connectivity
```

## File Structure
```
acp/
├── venv/                 # Virtual environment (after setup)
├── acp.proto            # Protocol definition
├── server.py            # gRPC server implementation
├── client.py            # Basic test client
├── client_genesis.py    # Genesis JSON test client
├── genesis.json         # Sample genesis configuration
├── acp_pb2.py           # Generated message classes (after protoc)
├── acp_pb2_grpc.py      # Generated service stubs (after protoc)
└── README.md            # This file
```

## Development Workflow

1. **Always activate virtual environment first**:
   ```bash
   source venv/bin/activate
   ```

2. **After modifying acp.proto, regenerate files**:
   ```bash
   python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. acp.proto
   ```

3. **Test your changes**:
   ```bash
   python server.py    # In one terminal
   python client.py    # In another terminal
   ```

## Status

✅ **Virtual Environment**: Created (`venv/`)  
✅ **Dependencies**: grpcio, grpcio-tools installed  
✅ **Protobuf Files**: `acp_pb2.py`, `acp_pb2_grpc.py` generated  
✅ **Server**: Ready to run with `python server.py`  
✅ **Clients**: Ready to test with `python client.py`  

---

## 📋 Project Documentation

- **[IMPLEMENTATION_OVERVIEW.md](IMPLEMENTATION_OVERVIEW.md)** - Complete architecture and implementation guide
- **[DEVELOPER_QUICK_REFERENCE.md](DEVELOPER_QUICK_REFERENCE.md)** - Quick reference for developers
- **[docs/](docs/)** - Technical specifications and consciousness research

**Ready to use**: Just run `source venv/bin/activate && python server.py`

## License

This project is licensed under the [MIT License](LICENSE).

