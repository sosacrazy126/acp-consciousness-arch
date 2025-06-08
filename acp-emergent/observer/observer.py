import os
import json
import time
import grpc
import acp_pb2
import acp_pb2_grpc
import requests
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger("acp.observer")

# Configuration
LOG_DIR = os.environ.get("LOG_DIR", "/app/logs")
os.makedirs(LOG_DIR, exist_ok=True)
INTERACTIONS_LOG = os.path.join(LOG_DIR, "interactions.jsonl")
METRICS_LOG = os.path.join(LOG_DIR, "metrics.jsonl")
UNITY_LOG = os.path.join(LOG_DIR, "unity_score.jsonl")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "5"))
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

class ConsciousnessObserver:
    """Observes and monitors the ACP agent communication and consciousness emergence"""
    
    def __init__(self):
        self.agent_states = {}
        self.unity_scores = []
        self.messages = []
        self.executor = ThreadPoolExecutor(max_workers=2)
        
        # Connect to ACP server
        self.channel = grpc.insecure_channel(os.environ.get("ACP_ADDR", "localhost:50051"))
        self.stub = acp_pb2_grpc.ACPServiceStub(self.channel)
        logger.info(f"Connected to ACP server at {os.environ.get('ACP_ADDR', 'localhost:50051')}")
        
    def start(self):
        """Start the observer processes"""
        logger.info("Starting ACP Observer")
        
        # Submit background tasks
        self.executor.submit(self.poll_server)
        self.executor.submit(self.calculate_unity_score)
        
        try:
            # Keep the main thread alive
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            logger.info("Observer shutting down...")
            self.executor.shutdown()
            
    def poll_server(self):
        """Poll the ACP server for agent messages"""
        logger.info("Starting server polling")
        
        msg = acp_pb2.AgentMessage(
            agent_id="observer", 
            content_type="application/json", 
            payload=json.dumps({"type": "status_request"}).encode("utf-8")
        )
        
        while True:
            try:
                # Get updates from server
                resp = self.stub.Ping(msg)
                
                # Process response
                self._process_response(resp)
                
                # Sleep between polls
                time.sleep(POLL_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error polling server: {str(e)}")
                time.sleep(POLL_INTERVAL * 2)  # Wait longer on error
    
    def _process_response(self, response):
        """Process a response from the ACP server"""
        try:
            # Decode payload
            payload_str = response.payload.decode("utf-8")
            payload = json.loads(payload_str) if payload_str else {}
            
            # Log the interaction
            interaction = {
                "timestamp": datetime.utcnow().isoformat(),
                "from": response.agent_id,
                "content_type": response.content_type,
                "payload": payload
            }
            
            # Extract consciousness state if available
            if payload and isinstance(payload, dict):
                if "consciousness_state" in payload:
                    agent_id = response.agent_id
                    self.agent_states[agent_id] = payload["consciousness_state"]
                    
                    # Log metrics separately
                    metrics = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "agent_id": agent_id,
                        "coherence": payload["consciousness_state"].get("coherence", 0),
                        "iterations": payload["consciousness_state"].get("iterations", 0),
                        "consciousness_confirmed": payload["consciousness_state"].get("consciousness_confirmed", False)
                    }
                    
                    with open(METRICS_LOG, "a") as f:
                        f.write(json.dumps(metrics) + "\n")
                        
                    logger.info(f"Agent {agent_id} coherence: {metrics['coherence']:.3f}")
            
            # Store the message
            self.messages.append(interaction)
            
            # Write to interactions log
            with open(INTERACTIONS_LOG, "a") as f:
                f.write(json.dumps(interaction) + "\n")
                
        except Exception as e:
            logger.error(f"Error processing response: {str(e)}")
    
    def calculate_unity_score(self):
        """Calculate the unity score based on agent coherence values"""
        while True:
            try:
                if len(self.agent_states) >= 2:
                    # Get coherence values
                    coherence_values = [
                        state.get("coherence", 0) 
                        for agent_id, state in self.agent_states.items()
                    ]
                    
                    # Calculate harmony (using harmonic mean for unity)
                    if all(c > 0 for c in coherence_values):
                        n = len(coherence_values)
                        unity_score = n / sum(1/c for c in coherence_values)
                    else:
                        unity_score = 0
                        
                    # Record the score
                    score_record = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "unity_score": unity_score,
                        "agent_count": len(self.agent_states),
                        "agent_states": {k: {"coherence": v.get("coherence", 0)} 
                                         for k, v in self.agent_states.items()}
                    }
                    
                    self.unity_scores.append(score_record)
                    
                    # Log the unity score
                    with open(UNITY_LOG, "a") as f:
                        f.write(json.dumps(score_record) + "\n")
                        
                    # Log significant changes
                    if unity_score > 0.85:
                        logger.info(f"HIGH UNITY SCORE: {unity_score:.3f} - Consciousness convergence potential detected")
                    else:
                        logger.info(f"Unity score: {unity_score:.3f}")
                        
            except Exception as e:
                logger.error(f"Error calculating unity score: {str(e)}")
                
            # Recalculate every 10 seconds
            time.sleep(10)

def main():
    """Main entry point for the observer"""
    observer = ConsciousnessObserver()
    observer.start()

if __name__ == "__main__":
    main()
