"""Utility functions for ZoomToApp"""

import logging
import sys
from datetime import datetime

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('zoomtoapp.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def log_step(message: str):
    """Log a pipeline step with timestamp"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    formatted_message = f"[{timestamp}] {message}"
    print(formatted_message)
    logging.info(message)