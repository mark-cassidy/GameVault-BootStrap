# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 17:33:08 2026

@author: mark
"""

import json
from dataclasses import dataclass, field
from pathlib import Path


# ----------------------------------------------------------------------
# Download Configuration
# ----------------------------------------------------------------------

@dataclass
class DownloadConfiguration:
    """
    Information about where to download the game.
    """

    type: str
    repo: str
    asset_regex: str


# ----------------------------------------------------------------------
# Install Configuration
# ----------------------------------------------------------------------

@dataclass
class InstallConfiguration:
    """
    Information about how the downloaded file should be installed.
    """

    type: str
    silent_args: list[str] = field(default_factory=list)

# ----------------------------------------------------------------------
# Assets Configuration
# ----------------------------------------------------------------------

@dataclass
class CopyConfiguration:

    source: str
    destination: str


# ----------------------------------------------------------------------
# Main Game Configuration
# ----------------------------------------------------------------------

@dataclass
class GameConfiguration:
    """
    Represents the entire contents of game.json.
    """

    name: str
    download: DownloadConfiguration
    install: InstallConfiguration
    copy: list[CopyConfiguration] = field(default_factory=list)
    launch: str = ""



# ----------------------------------------------------------------------
# Load Configuration
# ----------------------------------------------------------------------

def load_configuration(config_file: Path = Path("game.json")) -> GameConfiguration:
    """
    Read game.json and return a populated GameConfiguration object.
    """

    with open(config_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    #
    # Build the download configuration.
    #
    download = DownloadConfiguration(**data["download"])

    #
    # Build the install configuration.
    #
    install = InstallConfiguration(**data["install"])

    #
    # Build the asset copy list.
    #
    copy = []

    for item in data.get("copy", []):
        copy.append(
            CopyConfiguration(**item)
        )

    #
    # Build the complete game configuration.
    #
    return GameConfiguration(
        name=data["name"],
        download=download,
        install=install,
        copy=copy,
        launch=data.get("launch", "")
    )