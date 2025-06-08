FROM python:3.11-slim
WORKDIR /app
COPY acp_server/ ./acp_server/
COPY acp.proto ./
RUN pip install -r acp_server/requirements.txt
WORKDIR /app/acp_server
CMD ["python", "server.py"]
EXPOSE 50051
