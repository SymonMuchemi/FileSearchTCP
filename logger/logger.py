import logging

logger = logging.getLogger('Filesearch_tcp')

logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler('./log_files/details.log')
file_handler.setLevel(logging.DEBUG)

# Define log message format
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
