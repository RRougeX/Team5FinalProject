import logging
from transformers.utils import logging as transformers_logging


def cleanLogs():
    logging.disable(logging.CRITICAL)

    # Hide Hugging Face / Transformers progress bars
    transformers_logging.disable_progress_bar()