import logging,os
from datetime import datetime as dt

LOG_FILE = f"{os.getcwd()}/logs/{dt.now().strftime('%Y-%m-%d')}.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
if __name__ == "__main__":
    logger.info("Logging setup complete. Log file created at: %s", LOG_FILE)