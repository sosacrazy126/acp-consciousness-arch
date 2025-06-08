import os
import time
import requests
from pathlib import Path


def check_openrouter_api_key():
    """Check if OpenRouter API key is available"""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY environment variable not set")
        return False
    return True


def verify_openrouter_connection():
    """Verify connection to OpenRouter API"""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://agent-consciousness-protocol.com",
        "X-Title": "ACP Setup"
    }
    
    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return True
        else:
            print(f"ERROR: OpenRouter API returned status {response.status_code}")
            print(response.text)
            return False
    except requests.RequestException as e:
        print(f"ERROR connecting to OpenRouter: {str(e)}")
        return False


def check_model_availability(model):
    """Check if the specified model is available through OpenRouter"""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://agent-consciousness-protocol.com",
        "X-Title": "ACP Setup"
    }
    
    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            available_models = []
            for model_data in response.json().get("data", []):
                model_id = model_data.get("id")
                if model_id:
                    available_models.append(model_id)
            
            if model in available_models:
                print(f"✅ Model '{model}' is available on OpenRouter")
                return True
            else:
                print(f"⚠️ Model '{model}' not found. Available models include:")
                for avail_model in available_models[:10]:  # Show first 10 models
                    print(f"  - {avail_model}")
                return False
        else:
            print(f"ERROR: OpenRouter API returned status {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"ERROR retrieving models from OpenRouter: {str(e)}")
        return False


def test_model_generation(model):
    """Test generation with the model via OpenRouter"""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://agent-consciousness-protocol.com",
        "X-Title": "ACP Setup"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Testing connection for ACP: Say hello"}
        ],
        "max_tokens": 100
    }
    
    try:
        print(f"Testing generation with {model}...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            resp_json = response.json()
            if resp_json.get("choices") and len(resp_json["choices"]) > 0:
                content = resp_json["choices"][0]["message"]["content"]
                print(f"Model response: {content[:100]}...")  # Print first 100 chars
                return True
            else:
                print(f"ERROR: No content returned from model")
                return False
        else:
            print(f"ERROR: OpenRouter API returned status {response.status_code}")
            print(response.text)
            return False
    except requests.RequestException as e:
        print(f"ERROR testing model generation: {str(e)}")
        return False


def setup_openrouter():
    """Main setup function for OpenRouter configuration"""
    print("Setting up OpenRouter integration...")
    
    # Check API key
    if not check_openrouter_api_key():
        raise SystemExit("Missing OpenRouter API key. Please set OPENROUTER_API_KEY environment variable.")
    
    # Verify connection
    print("Verifying connection to OpenRouter...")
    if not verify_openrouter_connection():
        raise SystemExit("Failed to connect to OpenRouter API")
    
    # Check model availability
    model = os.environ.get("OPENROUTER_MODEL", "anthropic/claude-3-haiku")
    if not check_model_availability(model):
        print(f"WARNING: Specified model '{model}' may not be available")
        
    # Test generation
    if not test_model_generation(model):
        raise SystemExit("Failed to generate text with the specified model")
    
    print(f"✅ OpenRouter setup complete for model: {model}")
    print("You can now start the ACP system with the properly configured OpenRouter integration")


if __name__ == "__main__":
    setup_openrouter()