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

# Copy model setup utility and entrypoint
COPY scripts/setup_model.py /app/setup_model.py
COPY scripts/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Health check to verify Ollama connectivity
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from ollama_client import QwenClient; exit(0 if QwenClient().health_check() else 1)"

ENTRYPOINT ["/app/entrypoint.sh"]
