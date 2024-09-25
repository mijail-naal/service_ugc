from utils.logger import logger


def backoff_hadler(details: dict) -> None:
    """Backoff event handler logging function"""
    logger.info(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target.__name__} with args {args}"
        .format(**details)
    )
