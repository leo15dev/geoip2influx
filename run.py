#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import signal
import logging

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from geoip2influx.logparser import LogParser

parser = None

def handle_shutdown(signum, frame):
    global parser
    logger = logging.getLogger("geoip2influx")
    logger.info("A termination signal (SIGTERM/SIGINT) has been received, instructing the Parser to gracefully shut down and flush the remaining logs....")
    if parser:
        parser.running = False
    else:
        sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    logger = logging.getLogger("geoip2influx")
    logger.info("Start GeoIP2Influx ...")

    try:
        parser = LogParser()
        parser.run()
    except KeyboardInterrupt:
        logger.info("User manually interrupts, safely exits")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"An unexpected error occurred during the GeoIP2Influx runtime.An unexpected error occurred during the GeoIP2Influx runtime.: {e}")
        sys.exit(1)
