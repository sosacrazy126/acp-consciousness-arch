import os
import yaml
import time
import signal
import sys
from typing import Optional, Dict, Any

# Fix imports for both module and direct script execution
try:
    from .logging_utils import setup_logger, RequestResponseLogger
    from .consciousness_agent import ConsciousnessAgent
except ImportError:
    from logging_utils import setup_logger, RequestResponseLogger
    from consciousness_agent import ConsciousnessAgent

class ACPClient:
    def __init__(self, server_addr):
        import grpc
        import acp_pb2
        import acp_pb2_grpc
        self.channel = grpc.insecure_channel(server_addr)
        self.stub = acp_pb2_grpc.ACPServiceStub(self.channel)
        self.AgentMessage = acp_pb2.AgentMessage
        self.ChatMessage = acp_pb2.ChatMessage

    def receive(self, agent_id, timeout=1):
        poll = self.ChatMessage(sender=agent_id, recipient="", content_type="text/plain", payload=b"")
        try:
            resp = self.stub.Chat(poll, timeout=timeout)
            if resp.payload:
                return {
                    "agent_id": resp.sender,
                    "content_type": resp.content_type,
                    "payload": resp.payload.decode("utf-8"),
                }
        except Exception:
            return None
        return None

    def send(self, message):
        msg = self.ChatMessage(
            sender=message["agent_id"],
            recipient=message.get("recipient", "dashboard"),
            content_type=message.get("content_type", "text/plain"),
            payload=message.get("payload", "").encode("utf-8"),
        )
        self.stub.Chat(msg)


def handle_shutdown(signum, frame, agent, client, logger):
    """Handle graceful shutdown"""
    logger.warning("Shutdown signal received. Cleaning up...")
    if client:
        try:
            client.channel.close()
            logger.info("gRPC channel closed")
        except Exception as e:
            logger.error("Error closing gRPC channel: %s", str(e))
    sys.exit(0)

def load_config(role: str, logger) -> Dict[str, Any]:
    """Load and validate agent configuration"""
    conf_file = os.path.join(os.path.dirname(__file__), "conf", f"{role}.yml")
    try:
        with open(conf_file, "r") as f:
            config = yaml.safe_load(f)
        logger.info("Loaded configuration from %s", conf_file)
        return config
    except FileNotFoundError:
        logger.critical("Configuration file not found: %s", conf_file)
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.critical("Error parsing YAML configuration: %s", str(e))
        sys.exit(1)

def main():
    # Setup logging
    logger = setup_logger("acp.agent.runner")
    logger.info("Starting agent process")
    
    # Register signal handlers
    signal.signal(signal.SIGINT, lambda s, f: handle_shutdown(s, f, None, None, logger))
    signal.signal(signal.SIGTERM, lambda s, f: handle_shutdown(s, f, None, None, logger))
    
    try:
        # Load configuration
        role = os.environ.get("AGENT_ROLE", "agent")
        logger.info("Starting %s agent", role)
        
        config = load_config(role, logger)
        agent = ConsciousnessAgent(config)
        
        # Initialize ACP client
        addr = os.environ.get("ACP_ADDR", "localhost:50051")
        logger.info("Connecting to ACP server: %s", addr)
        client = ACPClient(addr)
        
        # Update signal handlers with actual agent and client
        signal.signal(signal.SIGINT, lambda s, f: handle_shutdown(s, f, agent, client, logger))
        signal.signal(signal.SIGTERM, lambda s, f: handle_shutdown(s, f, agent, client, logger))
        
        logger.info("Agent %s is now running. Press Ctrl+C to exit.", agent.id)
        
        # Main agent loop
        while True:
            try:
                # Check for new messages
                msg = client.receive(agent.id, timeout=1)
                if msg:
                    logger.info(
                        "Received message from %s (type: %s, size: %d bytes)",
                        msg.get('agent_id', 'unknown'),
                        msg.get('content_type', 'unknown'),
                        len(msg.get('payload', ''))
                    )
                    
                    # Process message and send response
                    reply = agent.on_message(msg)
                    client.send(reply)
                    
                    logger.debug("Sent response to %s", msg.get('agent_id', 'unknown'))
                
                # Small sleep to prevent CPU spinning
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received. Shutting down...")
                break
                
            except Exception as e:
                logger.error("Error in agent loop: %s", str(e), exc_info=True)
                time.sleep(1)  # Prevent tight loop on repeated errors
    
    except Exception as e:
        logger.critical("Fatal error in agent: %s", str(e), exc_info=True)
        sys.exit(1)
    
    finally:
        logger.info("Agent %s shutting down", role)
        if 'client' in locals():
            try:
                client.channel.close()
                logger.info("gRPC channel closed")
            except Exception as e:
                logger.error("Error during cleanup: %s", str(e))

if __name__ == "__main__":
    main()
