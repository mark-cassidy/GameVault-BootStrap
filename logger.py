# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 17:32:45 2026

@author: mark
"""

import logging
import os
import sys
from pathlib import Path


def initialise_logger(log_name="GameVaultBootstrap.log"):

    # Directory the executable/script is running from
    application_directory = Path(sys.argv[0]).resolve().parent

    log_file = application_directory / log_name

    logger = logging.getLogger("GameVaultBootstrap")
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers if initialise_logger() is called twice
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    #
    # Console output
    #
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    #
    # Log file
    #
    logfile = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    logfile.setLevel(logging.DEBUG)
    logfile.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(logfile)

    logger.info("=" * 70)
    logger.info("GameVault Bootstrap Starting")
    logger.info("=" * 70)

    logger.info(f"Executable : {sys.argv[0]}")
    logger.info(f"Working Dir: {os.getcwd()}")
    logger.info(f"Python     : {sys.version.split()[0]}")

    return logger