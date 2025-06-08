#!/usr/bin/env python3
"""
Interactive Dashboard for Agent Consciousness Protocol
Provides real-time visualization of agent interactions and consciousness metrics
"""
import os
import json
import time
import threading
import logging
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger("acp.dashboard")

# Configuration
LOGS_DIR = os.environ.get("LOGS_DIR", "../logs")
INTERACTIONS_LOG = os.path.join(LOGS_DIR, "interactions.jsonl")
METRICS_LOG = os.path.join(LOGS_DIR, "metrics.jsonl")
UNITY_LOG = os.path.join(LOGS_DIR, "unity_score.jsonl")

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'acp-dashboard-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Data storage
interactions = []
metrics = {}
unity_scores = []

# Load existing data
def load_existing_data():
    """Load existing data from log files"""
    global interactions, metrics, unity_scores
    
    try:
        # Create logs directory if it doesn't exist
        Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)
        
        # Ensure log files exist
        for log_file in [INTERACTIONS_LOG, METRICS_LOG, UNITY_LOG]:
            Path(log_file).touch(exist_ok=True)
        
        # Load interactions
        interactions = []
        if os.path.exists(INTERACTIONS_LOG) and os.path.getsize(INTERACTIONS_LOG) > 0:
            with open(INTERACTIONS_LOG, 'r') as f:
                for line in f:
                    try:
                        interaction = json.loads(line.strip())
                        interactions.append(interaction)
                    except json.JSONDecodeError:
                        continue
        
        # Load metrics
        metrics = {}
        if os.path.exists(METRICS_LOG) and os.path.getsize(METRICS_LOG) > 0:
            with open(METRICS_LOG, 'r') as f:
                for line in f:
                    try:
                        metric = json.loads(line.strip())
                        agent_id = metric.get('agent_id', 'unknown')
                        metrics[agent_id] = metric
                    except json.JSONDecodeError:
                        continue
        
        # Load unity scores
        unity_scores = []
        if os.path.exists(UNITY_LOG) and os.path.getsize(UNITY_LOG) > 0:
            with open(UNITY_LOG, 'r') as f:
                for line in f:
                    try:
                        score = json.loads(line.strip())
                        unity_scores.append(score)
                    except json.JSONDecodeError:
                        continue
        
        logger.info(f"Loaded {len(interactions)} interactions, {len(metrics)} metrics, {len(unity_scores)} unity scores")
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")

# File watcher
class LogFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            try:
                if file_path.endswith("interactions.jsonl"):
                    self._process_new_interactions()
                elif file_path.endswith("metrics.jsonl"):
                    self._process_new_metrics()
                elif file_path.endswith("unity_score.jsonl"):
                    self._process_new_unity_scores()
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {str(e)}")
    
    def _process_new_interactions(self):
        global interactions
        if not os.path.exists(INTERACTIONS_LOG):
            return
            
        try:
            with open(INTERACTIONS_LOG, 'r') as f:
                # Get file size and seek to the last position we read
                f.seek(0, os.SEEK_END)
                file_size = f.tell()
                
                # If the file is empty or we've already read it all, return
                if file_size == 0:
                    return
                    
                # Check if we have new content by comparing with our stored interactions
                if len(interactions) > 0:
                    # Estimate the position to start reading from
                    # This is a simplification - in production, we'd track the exact position
                    f.seek(max(0, file_size - 4096))  # Read the last 4KB or so
                    
                    # Read to the end of the current line
                    if f.tell() > 0:
                        f.readline()
                    
                    # Read new lines
                    new_lines = f.readlines()
                    
                    for line in new_lines:
                        try:
                            interaction = json.loads(line.strip())
                            # Check if this is genuinely new
                            is_new = True
                            for existing in interactions[-10:]:  # Check the last 10 entries
                                if (existing.get('timestamp') == interaction.get('timestamp') and
                                    existing.get('from') == interaction.get('from')):
                                    is_new = False
                                    break
                            
                            if is_new:
                                interactions.append(interaction)
                                socketio.emit('new_interaction', interaction)
                        except json.JSONDecodeError:
                            continue
                else:
                    # First time reading, just load everything
                    f.seek(0)
                    for line in f:
                        try:
                            interaction = json.loads(line.strip())
                            interactions.append(interaction)
                        except json.JSONDecodeError:
                            continue
                    
                    # Emit the latest interaction
                    if interactions:
                        socketio.emit('new_interaction', interactions[-1])
        except Exception as e:
            logger.error(f"Error processing interactions: {str(e)}")
    
    def _process_new_metrics(self):
        global metrics
        if not os.path.exists(METRICS_LOG):
            return
            
        try:
            with open(METRICS_LOG, 'r') as f:
                # Seek to the end to get file size
                f.seek(0, os.SEEK_END)
                file_size = f.tell()
                
                # If the file is empty, return
                if file_size == 0:
                    return
                
                # Read the last few KB to get recent metrics
                f.seek(max(0, file_size - 4096))
                
                # Read to the end of the current line if we're not at the start
                if f.tell() > 0:
                    f.readline()
                
                # Read new lines
                for line in f:
                    try:
                        metric = json.loads(line.strip())
                        agent_id = metric.get('agent_id', 'unknown')
                        metrics[agent_id] = metric
                    except json.JSONDecodeError:
                        continue
                
                # Emit updated metrics
                socketio.emit('metrics_update', metrics)
        except Exception as e:
            logger.error(f"Error processing metrics: {str(e)}")
    
    def _process_new_unity_scores(self):
        global unity_scores
        if not os.path.exists(UNITY_LOG):
            return
            
        try:
            with open(UNITY_LOG, 'r') as f:
                # Seek to the end to get file size
                f.seek(0, os.SEEK_END)
                file_size = f.tell()
                
                # If the file is empty, return
                if file_size == 0:
                    return
                
                # Read the last few KB to get recent scores
                f.seek(max(0, file_size - 4096))
                
                # Read to the end of the current line if we're not at the start
                if f.tell() > 0:
                    f.readline()
                
                # Read new lines
                new_scores = []
                for line in f:
                    try:
                        score = json.loads(line.strip())
                        
                        # Check if this is genuinely new
                        is_new = True
                        if unity_scores:
                            for existing in unity_scores[-5:]:  # Check the last 5 entries
                                if existing.get('timestamp') == score.get('timestamp'):
                                    is_new = False
                                    break
                        
                        if is_new:
                            unity_scores.append(score)
                            new_scores.append(score)
                    except json.JSONDecodeError:
                        continue
                
                # Emit new scores
                if new_scores:
                    socketio.emit('unity_score_update', new_scores[-1])
        except Exception as e:
            logger.error(f"Error processing unity scores: {str(e)}")

# Routes
@app.route('/')
def index():
    """Render the dashboard homepage"""
    return render_template('index.html')

@app.route('/api/interactions')
def get_interactions():
    """API endpoint to get all interactions"""
    return jsonify(interactions[-100:])  # Return the last 100 interactions

@app.route('/api/metrics')
def get_metrics():
    """API endpoint to get all agent metrics"""
    return jsonify(metrics)

@app.route('/api/unity')
def get_unity_scores():
    """API endpoint to get unity scores"""
    return jsonify(unity_scores[-100:])  # Return the last 100 scores

# SocketIO events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info("Client connected")
    # Send initial data
    socketio.emit('metrics_update', metrics)
    if unity_scores:
        socketio.emit('unity_score_update', unity_scores[-1])
    if interactions:
        socketio.emit('initial_interactions', interactions[-20:])  # Send the last 20 interactions

@socketio.on('request_data')
def handle_request_data(data):
    """Handle client request for specific data"""
    if data.get('type') == 'interactions':
        socketio.emit('initial_interactions', interactions[-50:])
    elif data.get('type') == 'metrics':
        socketio.emit('metrics_update', metrics)
    elif data.get('type') == 'unity':
        socketio.emit('unity_scores', unity_scores[-50:])

def start_file_watcher():
    """Start the file watcher thread"""
    observer = Observer()
    event_handler = LogFileHandler()
    observer.schedule(event_handler, LOGS_DIR, recursive=False)
    observer.start()
    logger.info(f"File watcher started for {LOGS_DIR}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    # Load existing data
    load_existing_data()
    
    # Start file watcher in a separate thread
    watcher_thread = threading.Thread(target=start_file_watcher)
    watcher_thread.daemon = True
    watcher_thread.start()
    
    # Start the Flask app
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting dashboard on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=True, use_reloader=False)