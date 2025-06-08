FROM python:3.11-slim
WORKDIR /app

# Copy proto file and generate protobuf code
COPY acp.proto .
RUN pip install --no-cache-dir grpcio grpcio-tools protobuf
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. acp.proto

# Copy application files
COPY observer/observer.py .
COPY observer/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "observer.py"]
