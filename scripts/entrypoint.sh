#!/bin/bash
set -e

python /app/setup_model.py
exec python /app/agents/run_agent.py
