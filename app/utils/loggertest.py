import logging

logger = logging.getLogger(__name__)  # Use a named logger

logging.basicConfig(level=logging.INFO)
logger.info('This should work')
