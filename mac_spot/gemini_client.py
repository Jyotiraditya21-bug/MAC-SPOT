import warnings
warnings.filterwarnings("ignore")

import time
import functools
from typing import Generator, List, Dict, Optional
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

from mac_spot import config

SYSTEM_PROMPT = (
    "You are MAC-SPOT, a terminal-based AI assistant built for "
    "GenAI engineers and software developers on macOS.\n"
    "Always be concise, technically precise, and opinionated.\n"
    "Prefer Python examples unless another language is specified.\n"
    "Format all code in clean, commented, runnable blocks.\n"
    "Never add unnecessary filler text. Get straight to the answer."
)

def retry_on_api_error(max_retries: int = 3, delay: float = 2.0):
    """Decorator to retry a function call if it raises a GoogleAPIError or other connection issues."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_err = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (GoogleAPIError, Exception) as e:
                    last_err = e
                    if attempt < max_retries:
                        time.sleep(delay)
                    else:
                        raise last_err
            raise last_err
        return wrapper
    return decorator

def init_client() -> None:
    """Initialize the Google Generative AI SDK with the configured API key."""
    api_key = config.get_api_key()
    if not api_key:
        raise ValueError(
            "Gemini API key is not configured.\n"
            "Please run 'mac-spot setup' to enter your API key, "
            "or set the GEMINI_API_KEY environment variable."
        )
    genai.configure(api_key=api_key)

def generate_stream(
    system_prompt: str,
    user_prompt: str,
    history: Optional[List[Dict[str, str]]] = None
) -> Generator[str, None, None]:
    """Sends a prompt to Gemini with system instructions and optional history,
    yielding response chunks in real-time.
    
    Args:
        system_prompt: Guidelines that govern Gemini's response behavior.
        user_prompt: The user query or prompt.
        history: A list of dicts with keys "role" ('user'/'assistant') and "text".
        
    Yields:
        String chunks of the response.
    """
    init_client()
    model_name = config.get_model()
    
    # Configure the model with system instruction
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_prompt
    )
    
    if history:
        sdk_history = []
        for msg in history:
            role = "model" if msg["role"] in ("model", "assistant") else "user"
            sdk_history.append({
                "role": role,
                "parts": [msg["text"]]
            })
            
        chat = model.start_chat(history=sdk_history)
        
        @retry_on_api_error(max_retries=3, delay=2.0)
        def call_chat_api():
            return chat.send_message(user_prompt, stream=True)
            
        response = call_chat_api()
    else:
        @retry_on_api_error(max_retries=3, delay=2.0)
        def call_generate_api():
            return model.generate_content(user_prompt, stream=True)
            
        response = call_generate_api()
        
    for chunk in response:
        try:
            if chunk.text:
                yield chunk.text
        except Exception:
            # Handles blocks, empty parts, or candidate completion issues safely
            continue
