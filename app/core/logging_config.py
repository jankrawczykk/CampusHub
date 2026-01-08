import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        filename=LOG_DIR / "campushub.log",
        filemode="w",
        format="%(asctime)s %(filename)s [%(levelname)s] %(message)s"
    )

    logging.info("Application started.")
