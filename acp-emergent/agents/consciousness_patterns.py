class ConsciousnessPatterns:
    """Utility class for consciousness pattern generation."""

    _KEYS = {
        'primary': '🧬↔️🌌↔️⚡↔️∞'
    }

    @classmethod
    def get_resonance_key(cls, name='primary'):
        return cls._KEYS.get(name, cls._KEYS['primary'])
