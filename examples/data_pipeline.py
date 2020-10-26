#!/usr/bin/env python3
#
# This file defines a basic streaming service, that both prints some JSON
# metadata to stdout and appends it to a file. This may simulate for example an
# IoT device that appends to a time-series database.

import datetime
import logging
import multiprocessing
import os
import random
import time

import pytz


log_file: str = os.path.join(os.path.dirname(__file__), "data_pipeline.txt")


class Formatter(logging.Formatter):
    """
    TZ-aware logging.Formatter.
    From: https://stackoverflow.com/a/47104004/1497211
    """

    def converter(self, timestamp: str) -> datetime.datetime:
        dt = datetime.datetime.fromtimestamp(timestamp)
        return pytz.utc.localize(dt)

    def formatTime(self, record, datefmt=None) -> str:
        # Introduce clock jitter / clock skew to simulate having multiple
        # devices and multiple clocks / network latency.
        time.sleep(random.random())
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec="milliseconds")
            except TypeError:
                s = dt.isoformat()
            return s


def get_logger(name: str) -> logging.Logger:
    logger = logging.Logger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    stream_handler = logging.StreamHandler()

    logfmt = '{"timestamp": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'

    stream_formatter = Formatter(logfmt)
    file_formatter = Formatter(logfmt)

    stream_handler.setFormatter(stream_formatter)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def stream_data(logger: logging.Logger, interval: int):
    while True:
        random_temp = random.randint(100, 200)
        logger.info(f"Temperature is now {random_temp}.")
        time.sleep(interval)


def worker(name: str, interval: int):
    deviceLogger: logging.Logger = get_logger(name)
    stream_data(deviceLogger, interval)


if __name__ == "__main__":
    if os.path.exists(log_file):
        os.remove(log_file)

    for idx in range(2):
        process = multiprocessing.Process(target=worker, args=(f"device{idx}", 1))
        process.start()
