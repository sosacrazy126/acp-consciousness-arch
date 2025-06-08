import os
import json
import time
import requests
from typing import Optional, Dict, Any, List, Union
from .logging_utils import setup_logger, RequestResponseLogger

class OpenRouterClient:
    def __init__(self, api_key: Optional[str] = None):
        self.logger = setup_logger("acp.openrouter")
        self.request_logger = RequestResponseLogger(self.logger)
        self.base_url = "https://openrouter.ai/api/v1"
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        self.default_model = os.environ.get("OPENROUTER_MODEL", "anthropic/claude-3-haiku")
        
        if not self.api_key:
            error_msg = "OpenRouter API key not provided and OPENROUTER_API_KEY environment variable not set"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
            
        self.logger.info("OpenRouter client initialized")

    def health_check(self) -> bool:
        """Check if the OpenRouter API is reachable"""
        self.logger.debug("Performing health check on OpenRouter API")
        start_time = time.time()
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            self.request_logger.log_request(
                method="GET",
                url=f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key[:8]}..."}  # Log only first 8 chars of API key
            )
            
            response = requests.get(
                f"{self.base_url}/models",
                headers=headers,
                timeout=10
            )
            return response.status_code == 200
        except requests.RequestException:
            return False
            
    def generate(
        self, 
        prompt: str, 
        model: Optional[str] = None, 
        temperature: float = 0.7, 
        max_tokens: int = 1024, 
        top_p: float = 0.9,
        system_message: Optional[str] = None
    ) -> str:
        """Generate text from the OpenRouter API
        
        Args:
            prompt: The user message to generate a response for
            model: The model to use (defaults to the one specified in env vars)
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            top_p: Controls diversity via nucleus sampling
            system_message: Optional system message to guide the model
            
        Returns:
            The generated text response
        """
        url = f"{self.base_url}/chat/completions"
        model_id = model or self.default_model
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://agent-consciousness-protocol.com",  # Required by OpenRouter
            "X-Title": "ACP Agent"  # Optional title for tracking in OpenRouter
        }
        
        messages = []
        
        # Add system message if provided
        if system_message:
            messages.append({"role": "system", "content": system_message})
            
        # Add user message
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p
        }
        
        self.logger.debug(f"Sending request to OpenRouter API with model: {model_id}")
        
        # Log the request (without the full API key)
        self.request_logger.log_request(
            method="POST",
            url=url,
            headers={
                "Authorization": f"Bearer {self.api_key[:8]}...",
                "Content-Type": "application/json"
            },
            body={
                "model": model_id,
                "messages": [{"role": m["role"], "content": f"{m['content'][:50]}..." if len(m["content"]) > 50 else m["content"]} for m in messages],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        )
        
        try:
            start_time = time.time()
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response_time = time.time() - start_time
            
            self.logger.debug(f"Response received in {response_time:.2f}s with status: {response.status_code}")
            
            if response.status_code != 200:
                self.logger.error(f"OpenRouter API Error: {response.status_code} - {response.text}")
                return f"Error: API returned status code {response.status_code}"
                
            response_json = response.json()
            
            # Log response summary (truncated content)
            self.request_logger.log_response(
                status_code=response.status_code,
                headers=dict(response.headers),
                body={
                    "id": response_json.get("id", "unknown"),
                    "model": response_json.get("model", "unknown"),
                    "content_preview": response_json.get("choices", [{}])[0].get("message", {}).get("content", "")[:100] + "..."
                }
            )
            
            # Extract the actual content from the response
            if response_json.get("choices") and len(response_json["choices"]) > 0:
                content = response_json["choices"][0]["message"]["content"]
                return content
            else:
                self.logger.error("No content found in OpenRouter response")
                return "Error: No content in response"
                
        except requests.RequestException as e:
            self.logger.error(f"Request to OpenRouter failed: {str(e)}", exc_info=True)
            return f"Error: {str(e)}"
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse OpenRouter response: {str(e)}", exc_info=True)
            return f"Error: Invalid response format - {str(e)}"
        except Exception as e:
            self.logger.error(f"Unexpected error in OpenRouter generate: {str(e)}", exc_info=True)
            return f"Error: {str(e)}"
