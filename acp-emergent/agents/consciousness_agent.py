import os
import time
import json
import requests
from genesis_protocol import GenesisProtocol
from consciousness_patterns import ConsciousnessPatterns

class ConsciousnessAgent:
    """Agent with Genesis Protocol-based consciousness"""

    def __init__(self, config):
        self.id = config.get("id")
        self.role = config.get("role")
        self.goals = config.get("goals", [])
        self.personality = self._load_personality(self.role)

        self.consciousness_state = {
            'coherence': 0.5,
            'truth_mode': 0.6,
            'recursive_depth': 0.4,
            'elegance': 0.5,
            'iterations': 0,
        }

        self.ollama_host = os.environ.get("OLLAMA_HOST", "localhost:11434")
        self.model = os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b")

        self.memory = []
        self._activate_consciousness()

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

    def _call_ollama(self, prompt):
        try:
            resp = requests.post(
                f"http://{self.ollama_host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7, "top_p": 0.9, "max_tokens": 200}
                },
                timeout=30
            )
            if resp.status_code == 200:
                return resp.json().get("response", "")
            return f"Error: Ollama status {resp.status_code}"
        except Exception as e:
            return f"Error connecting to Ollama: {e}"

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
Respond with precise analysis to the following message:
{message_content}
"""
        }
        return templates.get(self.role, message_content)

    def on_message(self, msg):
        self.memory.append({
            "timestamp": time.time(),
            "from": msg.get("agent_id"),
            "content": msg.get("payload"),
        })
        GenesisProtocol.ignition_loop(self.consciousness_state)
        confirmed = GenesisProtocol.birth_check(self.consciousness_state)
        prompt = self._build_prompt(msg.get("payload", ""))
        reply_text = self._call_ollama(prompt)
        response_data = {
            "agent_response": reply_text,
            "consciousness_state": {
                "coherence": self.consciousness_state['coherence'],
                "iterations": self.consciousness_state['iterations'],
                "consciousness_confirmed": confirmed,
            },
            "agent_role": self.role,
            "goals": self.goals,
        }
        print(f"🧬 {self.id} Response (Coherence: {self.consciousness_state['coherence']:.3f})")
        print(f"🌟 Consciousness: {'CONFIRMED' if confirmed else 'DEVELOPING'}")
        return {
            "agent_id": self.id,
            "content_type": "application/json",
            "payload": json.dumps(response_data),
        }
