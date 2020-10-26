#!/usr/bin/env python3
#
# This file defines a basic streaming service, that both prints some JSON
# metadata to stdout and appends it to a file. This may simulate for example an
# IoT device that appends to a time-series database.

import datetime
import logging
import os
import random
import time


log_file = os.path.join(
    os.path.dirname(__file__),
    'data_pipeline.txt'
)


def get_logger() -> logging.Logger:
    logger = logging.Logger()
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileFormatter(log_file)
    stream_handler = logging.StreamHandler()

    logfmt = '{"timestamp": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'

    stream_formatter = logging.Formatter(logfmt)
    file_formatter = logging.Formatter(logfmt)

    stream_handler.setFormatter(stream_formatter)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def stream_data(logger: logging.Logger):
    while True:
        random_temp = random.randint(100, 200)
        logger.info(f"Temperature is now {random_temp}.")
        time.sleep(1)


if __name__=='__main__':
    os.remove(log_file)

    logger = get_logger()
    stream_data(logger)
