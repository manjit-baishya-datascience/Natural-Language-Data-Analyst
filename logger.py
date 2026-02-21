import logging
import os
import datetime


def get_logger(name: str = "llm_data_app", logs_dir: str = "logs") -> logging.Logger:
    os.makedirs(logs_dir, exist_ok=True)
    fname = datetime.date.today().isoformat() + ".log"
    path = os.path.join(logs_dir, fname)

    logger = logging.getLogger(name)
    if getattr(logger, "_configured", False):
        return logger

    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

    fh = logging.FileHandler(path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # mark configured so repeated imports don't add handlers
    logger._configured = True
    return logger
