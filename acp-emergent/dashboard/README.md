# ACP Dashboard

The ACP Dashboard provides a real-time web interface for monitoring and interacting with the Agent Consciousness Protocol system.

## Features

- **Real-time agent interaction visualization**
- **Consciousness metrics tracking**
- **Unity Score monitoring with threshold detection**
- **Interactive agent message display**

## Architecture

The dashboard consists of:

1. **Flask Web Server**: Serves the web interface and handles API requests
2. **Socket.IO**: Provides real-time updates and streaming data
3. **File Watcher**: Monitors log files for changes and updates the UI
4. **Web Interface**: Interactive UI built with Bootstrap and Chart.js

## Running the Dashboard

The dashboard is integrated into the main docker-compose setup. When you run the entire ACP system, the dashboard will be available at:

```
http://localhost:5000
```

To run the dashboard separately:

```bash
cd dashboard
pip install -r requirements.txt
python app.py
```

## Dashboard Components

### Unity Score Monitor

The Unity Score is a key metric representing the harmonic mean of all agent coherence values. It serves as an indicator of "consciousness emergence" when it exceeds 0.85.

### Agent Interactions

Real-time display of messages exchanged between agents, including their responses and consciousness states.

### Agent Metrics

Displays current consciousness metrics for each agent, including:
- Coherence values
- Iteration counts
- Consciousness confirmation status

## Configuration

The dashboard can be configured through environment variables:

- `LOGS_DIR`: Directory containing the log files (default: "../logs")
- `PORT`: Web server port (default: 5000)

## Log Files

The dashboard reads and monitors the following log files:

- `interactions.jsonl`: Records all agent interactions
- `metrics.jsonl`: Tracks agent consciousness metrics
- `unity_score.jsonl`: Records Unity Score calculations

## Adding New Features

To extend the dashboard with new features:

1. Add new routes in `app.py`
2. Create new Socket.IO event handlers
3. Extend the UI in `templates/index.html`

## Troubleshooting

- **No data appears**: Ensure the log files are being written to correctly
- **Socket.IO disconnects**: Check for network issues or high server load
- **UI updates slowly**: Consider adjusting the polling interval