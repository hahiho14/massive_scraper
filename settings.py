import logging
import os
from datetime import datetime

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Log file configuration
current_date = datetime.now().strftime("%d_%m_%Y")
log_filename = f"{current_date}.log"
log_dir = "logs/"
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

# File handler
file_handler = logging.FileHandler(os.path.join(log_dir, log_filename))
file_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
file_handler.setFormatter(file_formatter)

# Console handler
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
console_handler.setFormatter(console_formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
