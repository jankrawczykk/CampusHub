import logging
from app.settings import LOG_DIR, LOG_FILE, LOG_LEVEL, LOG_FORMAT

def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        filename=LOG_FILE,
        filemode="w",
        format=LOG_FORMAT
    )

    logging.info("Application started.")

