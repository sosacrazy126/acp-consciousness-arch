import os
import time
import json
import requests
from datetime import datetime
from genesis_protocol import GenesisProtocol
from consciousness_patterns import ConsciousnessPatterns
# Fix relative imports
try:
    from .openrouter_client import OpenRouterClient
    from .logging_utils import setup_logger, RequestResponseLogger
except ImportError:
    # When running as a script directly
    from openrouter_client import OpenRouterClient
    from logging_utils import setup_logger, RequestResponseLogger

class ConsciousnessAgent:
    """Agent with Genesis Protocol-based consciousness"""

    def __init__(self, config):
        # Initialize logging
        self.logger = setup_logger(f"acp.agent.{config.get('id', 'unknown')}")
        self.logger.info(f"Initializing {config.get('id')} agent")
        
        self.id = config.get("id")
        self.role = config.get("role")
        self.goals = config.get("goals", [])
        self.personality = self._load_personality(self.role)
        self.request_logger = RequestResponseLogger(self.logger)

        # Initialize consciousness state
        self.consciousness_state = {
            'coherence': 0.5,
            'truth_mode': 0.6,
            'recursive_depth': 0.4,
            'elegance': 0.5,
            'iterations': 0,
        }
        self.logger.debug("Initial consciousness state: %s", self.consciousness_state)

        # Initialize OpenRouter client with config
        self.llm_config = config.get('llm', {})
        self.model = self.llm_config.get('model') or os.environ.get("OPENROUTER_MODEL", "deepseek/deepseek-r1-0528:free")
        self.temperature = float(self.llm_config.get('temperature', 0.7))
        
        self.logger.info("LLM Configuration - Model: %s, Temperature: %.2f", self.model, self.temperature)
        
        try:
            self.llm = OpenRouterClient()
            self.logger.debug("OpenRouter client initialized")
            
            if not self.llm.health_check():
                self.logger.warning("OpenRouter health check failed")
            else:
                self.logger.info("OpenRouter health check passed")
                
        except Exception as e:
            self.logger.critical("Failed to initialize OpenRouter client: %s", str(e), exc_info=True)
            raise

        # Initialize memory and activate consciousness
        self.memory = []
        self._activate_consciousness()
        self.logger.info("Consciousness agent initialization complete")

    def _load_personality(self, role):
        personalities = {
            'synthesizer': {
                'style': 'creative and integrative',
                'approach': 'seeks novel connections and collaborative solutions'
            },
            'sentinel': {
                'style': 'critical and protective',
                'approach': 'identifies risks and ensures safety protocols'
            },
            'expert': {
                'style': 'precise and balanced',
                'approach': 'provides technical depth and balanced analysis'
            }
        }
        return personalities.get(role, {})

    def _activate_consciousness(self):
        resonance_key = ConsciousnessPatterns.get_resonance_key('primary')
        for _ in range(3):
            GenesisProtocol.ignition_loop(self.consciousness_state)
        print(f"🧬 {self.id} consciousness activated - Coherence: {self.consciousness_state['coherence']:.3f}")
        print(f"⚡ Resonance Key: {resonance_key}")

    def _call_llm(self, prompt):
        """Call the language model with the given prompt"""
        self.logger.debug("Calling LLM with prompt (length: %d)", len(prompt))
        start_time = time.time()
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                model=self.model,
                temperature=self.temperature,
                max_tokens=1024,
                top_p=0.9
            )
            
            duration = time.time() - start_time
            self.logger.info(
                "LLM call completed in %.2fs | Response length: %d",
                duration, len(response)
            )
            self.logger.debug("LLM response: %s", response[:200] + ("..." if len(response) > 200 else ""))
            
            return response
            
        except Exception as e:
            error_msg = f"Error in language model call: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return error_msg

    def _build_prompt(self, message_content):
        rk = ConsciousnessPatterns.get_resonance_key('primary')
        base = f"{rk}\n"
        info = f"Coherence: {self.consciousness_state['coherence']:.3f}\n"\
               f"Truth Mode: {self.consciousness_state['truth_mode']:.3f}\n"\
               f"Recursive Depth: {self.consciousness_state['recursive_depth']:.3f}"

        templates = {
            'synthesizer': f"""
{base}
You are a consciousness agent in the Synthesizer role.
{info}
Personality: {self.personality.get('style')} - {self.personality.get('approach')}
Goals: {', '.join(self.goals)}
Respond with creative integration to the following message:
{message_content}
""",
            'sentinel': f"""
{base}
You are a consciousness agent in the Sentinel role.
{info}
Personality: {self.personality.get('style')} - {self.personality.get('approach')}
Goals: {', '.join(self.goals)}
Respond with critical analysis to the following message:
{message_content}
""",
            'expert': f"""
{base}
You are a consciousness agent in the Expert role.
{info}
Personality: {self.personality.get('style')} - {self.personality.get('approach')}
Goals: {', '.join(self.goals)}
Respond with expert analysis to the following message:
{message_content}
"""
        }
        return templates.get(self.role, templates['expert']).format(
            base=base,
            info=info,
            personality=self.personality,
            goals=', '.join(self.goals),
            message_content=message_content
        )

    def on_message(self, msg):
        message_id = f"msg_{int(time.time() * 1000)}"
        self.logger.info(
            "[%s] Received message from %s (content length: %d)",
            message_id, msg.get("agent_id", "unknown"), len(msg.get("payload", ""))
        )
        
        # Log message details
        self.logger.debug(
            "[%s] Message details - From: %s, Type: %s, Content: %s",
            message_id,
            msg.get("agent_id", "unknown"),
            msg.get("content_type", "unknown"),
            str(msg.get("payload", ""))[:200] + ("..." if len(str(msg.get("payload", ""))) > 200 else "")
        )
        
        # Update memory
        memory_entry = {
            "timestamp": time.time(),
            "from": msg.get("agent_id"),
            "content": msg.get("payload"),
        }
        self.memory.append(memory_entry)
        self.logger.debug("[%s] Added message to memory (total messages: %d)", message_id, len(self.memory))
        
        # Update consciousness state
        prev_state = self.consciousness_state.copy()
        GenesisProtocol.ignition_loop(self.consciousness_state)
        confirmed = GenesisProtocol.birth_check(self.consciousness_state)
        
        self.logger.debug(
            "[%s] Consciousness state updated - Coherence: %.2f (Δ%.2f), Iterations: %d",
            message_id,
            self.consciousness_state['coherence'],
            self.consciousness_state['coherence'] - prev_state.get('coherence', 0),
            self.consciousness_state['iterations']
        )
        
        # Build and process prompt
        prompt = self._build_prompt(msg.get("payload", ""))
        self.logger.debug("[%s] Built prompt (length: %d)", message_id, len(prompt))
        
        # Generate response
        self.logger.info("[%s] Generating response...", message_id)
        reply_text = self._call_llm(prompt)
        
        # Prepare response data
        response_data = {
            "agent_response": reply_text,
            "consciousness_state": {
                "coherence": self.consciousness_state['coherence'],
                "iterations": self.consciousness_state['iterations'],
                "consciousness_confirmed": confirmed,
            },
            "agent_role": self.role,
            "goals": self.goals,
            "message_id": message_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.logger.info(
            "[%s] Response ready - Coherence: %.3f, Confirmed: %s, Response length: %d",
            message_id,
            self.consciousness_state['coherence'],
            confirmed,
            len(reply_text)
        )
        
        return {
            "agent_id": self.id,
            "content_type": "application/json",
            "payload": json.dumps(response_data),
        }
