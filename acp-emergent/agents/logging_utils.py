import logging
import sys
from typing import Optional, Dict, Any
from datetime import datetime

class RichFormatter(logging.Formatter):
    """Custom formatter with rich colors and formatting"""
    
    # ANSI color codes
    GREY = "\x1b[38;20m"
    BLUE = "\x1b[34;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"
    
    FORMATS = {
        logging.DEBUG: f"{GREY}%(asctime)s - %(name)s - %(levelname)s - %(message)s{RESET}",
        logging.INFO: f"{BLUE}%(asctime)s - %(name)s - %(levelname)s - %(message)s{RESET}",
        logging.WARNING: f"{YELLOW}%(asctime)s - %(name)s - %(levelname)s - %(message)s{RESET}",
        logging.ERROR: f"{RED}%(asctime)s - %(name)s - %(levelname)s - %(message)s{RESET}",
        logging.CRITICAL: f"{BOLD_RED}%(asctime)s - %(name)s - %(levelname)s - %(message)s{RESET}",
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS[logging.INFO])
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

def setup_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    """Set up a logger with rich formatting"""
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Prevent adding multiple handlers
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(RichFormatter())
        logger.addHandler(console_handler)
    
    return logger

class RequestResponseLogger:
    """Utility class for logging HTTP requests and responses"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_request(self, method: str, url: str, headers: Optional[Dict] = None, body: Any = None):
        """Log HTTP request details"""
        self.logger.debug("\n" + "=" * 80)
        self.logger.debug(f"REQUEST: {method} {url}")
        self.logger.debug("HEADERS: %s", headers)
        if body:
            self.logger.debug("BODY: %s", body)
    
    def log_response(self, response):
        """Log HTTP response details"""
        self.logger.debug(f"RESPONSE: {response.status_code}")
        try:
            self.logger.debug("RESPONSE BODY: %s", response.json())
        except ValueError:
            self.logger.debug("RESPONSE TEXT: %s", response.text)
        self.logger.debug("=" * 80 + "\n")

# Create a default logger instance
default_logger = setup_logger("acp")

# Example usage:
# logger = setup_logger(__name__)
# logger.info("This is an info message")
# logger.error("This is an error message")
