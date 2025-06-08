FROM python:3.11-slim
WORKDIR /app

# Copy proto file and generate protobuf code
COPY acp.proto .
RUN pip install --no-cache-dir grpcio-tools
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. acp.proto

# Copy application files
COPY agents/ ./agents/
COPY genesis_protocol.py .

WORKDIR /app/agents
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for Ollama client
RUN pip install --no-cache-dir requests urllib3

CMD ["python", "run_agent.py"]
