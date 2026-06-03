import os

CONFIG_DIR = os.path.expanduser("~/.mac-spot")
API_KEY_FILE = os.path.join(CONFIG_DIR, "api_key")
DEFAULT_MODEL = "gemini-3.5-flash"

def get_api_key() -> str | None:
    """Retrieve the Gemini API key, giving preference to the GEMINI_API_KEY 
    environment variable, falling back to the saved file config.
    """
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key
    
    if os.path.exists(API_KEY_FILE):
        try:
            with open(API_KEY_FILE, "r") as f:
                return f.read().strip()
        except Exception:
            return None
    return None

def get_model() -> str:
    """Retrieve the model name, defaulting to gemini-1.5-flash unless overridden
    by the MAC_SPOT_MODEL environment variable.
    """
    return os.environ.get("MAC_SPOT_MODEL", DEFAULT_MODEL)

def save_api_key(api_key: str) -> None:
    """Save the API key to ~/.mac-spot/api_key and set file permissions to 600."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, mode=0o700, exist_ok=True)
    
    with open(API_KEY_FILE, "w") as f:
        f.write(api_key.strip())
        
    os.chmod(API_KEY_FILE, 0o600)
