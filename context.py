# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 17:31:51 2026

@author: mark
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class BootstrapContext:

    install_directory: Path
    package_directory: Path
    config: object
    logger: object