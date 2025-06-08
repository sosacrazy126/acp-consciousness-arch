FROM python:3.11-slim
WORKDIR /app
COPY agents/ ./agents/
WORKDIR /app/agents
RUN pip install -r requirements.txt
CMD ["python", "run_agent.py"]
