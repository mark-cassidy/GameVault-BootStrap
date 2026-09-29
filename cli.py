# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 17:30:18 2026

@author: mark
"""

import argparse
from pathlib import Path


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--install-dir",
        required=True,
        help="Directory supplied by GameVault"
    )

    args, unknown = parser.parse_known_args()

    args.install_dir = Path(args.install_dir)
    args.unknown = unknown

    return args