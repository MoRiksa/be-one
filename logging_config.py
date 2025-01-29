# logging_config.py

import logging
from logging.config import dictConfig


def setup_logging():
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "console": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
                "file": {
                    "level": "DEBUG",
                    "class": "logging.FileHandler",
                    "filename": "app.log",  # File log akan disimpan di sini
                    "formatter": "default",
                },
            },
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(levelname)s - %(message)s",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["console", "file"],
                    "level": "DEBUG",  # Bisa diubah sesuai kebutuhan
                    "propagate": True,
                },
            },
        }
    )
