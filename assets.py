# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 20:20:44 2026

@author: mark
"""

import shutil
from pathlib import Path

from config import CopyConfiguration


class AssetManager:

    def __init__(self, logger):

        self.logger = logger

    def copy_assets(
        self,
        package_directory: Path,
        install_directory: Path,
        assets: list[CopyConfiguration]
    ):

        if not assets:

            self.logger.info("")
            self.logger.info("No assets to copy.")

            return

        self.logger.info("")
        self.logger.info("Copying Assets")
        self.logger.info("--------------")

        for asset in assets:

            source = package_directory / asset.source
            destination = install_directory / asset.destination

            self.logger.info(f"{source}")
            self.logger.info(f" -> {destination}")

            if source.is_dir():

                shutil.copytree(
                    source,
                    destination,
                    dirs_exist_ok=True
                )

            else:

                destination.mkdir(
                    parents=True,
                    exist_ok=True
                )

                shutil.copy2(
                    source,
                    destination
                )

        self.logger.info("")
        self.logger.info("Assets copied successfully.")