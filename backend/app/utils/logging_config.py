import logging
import sys
from app.core.config import settings

def setup_logging():
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Configure logging formatter and handler
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True
    )
    
    # Return root logger or a specific logger
    logger = logging.getLogger("house_price_api")
    logger.setLevel(log_level)
    return logger

logger = setup_logging()
