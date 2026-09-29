# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 17:29:31 2026

@author: mark

bootstrap.py

Entry point for the GameVault Bootstrap.

Current responsibilities:

1. Parse command-line arguments
2. Load game.json
3. Initialise logging
4. Determine package directory
5. Query GitHub
6. Display the selected release
"""

from pathlib import Path
import sys

from cli import parse_arguments
from config import load_configuration
from context import BootstrapContext
from github import GithubClient
from logger import initialise_logger
from downloader import Downloader
from installer import Installer
from assets import AssetManager


def main():

    #
    # Read command-line arguments.
    #
    args = parse_arguments()

    #
    # Create the logger.
    #
    logger = initialise_logger()

    #
    # Load game.json
    #
    config = load_configuration()

    #
    # Determine where this executable/script is located.
    #
    if getattr(sys, "frozen", False):
        package_directory = Path(sys.executable).parent
    else:
        package_directory = Path(__file__).parent

    #
    # Build the runtime context.
    #
    context = BootstrapContext(
        install_directory=args.install_dir,
        package_directory=package_directory,
        config=config,
        logger=logger
    )

    #
    # Display bootstrap information.
    #
    logger.info("")
    logger.info("Bootstrap Context")
    logger.info("-----------------")
    logger.info(f"Game              : {config.name}")
    logger.info(f"Install Directory : {context.install_directory}")
    logger.info(f"Package Directory : {context.package_directory}")

    #
    # Display command line.
    #
    logger.info("")
    logger.info("Command Line")
    logger.info("------------")

    for arg in sys.argv:
        logger.info(arg)

    #
    # Connect to GitHub.
    #
    logger.info("")
    logger.info("Connecting to GitHub...")

    github = GithubClient()

    release = github.latest_release(
        config.download.repo
    )

    asset = github.find_asset(
        release,
        config.download.asset_regex
    )

    #
    # Display release information.
    #
    logger.info("")
    logger.info("Latest Release")
    logger.info("--------------")
    logger.info(f"Tag       : {release.tag}")
    logger.info(f"Name      : {release.name}")
    logger.info(f"Published : {release.published}")

    logger.info("")
    logger.info("Selected Asset")
    logger.info("--------------")
    logger.info(f"Name : {asset.name}")
    logger.info(f"Size : {asset.size:,} bytes")
    logger.info(f"URL  : {asset.download_url}")

    logger.info("")
    logger.info("Finished.")
    
    #
    # Download the asset
    #

    downloader = Downloader(logger)

    #
    # Create the install directory if it doesn't already exist.
    #
    context.install_directory.mkdir(
        parents=True,
        exist_ok=True
        )

    #
    # Create a Downloads folder inside the installation directory.
    #
    download_folder = (
        context.install_directory /
        "Downloads"
        )

    downloaded_file = downloader.download(
        asset.download_url,
        download_folder
        )

    logger.info("")
    logger.info(f"Downloaded to:")

    logger.info(downloaded_file)
    
    #
    # Install the game.
    #

    installer = Installer(logger)

    installer.install(
        downloaded_file,
        context.install_directory,
        config.install
        )
    assets = AssetManager(logger)

    assets.copy_assets(
        context.package_directory,
        context.install_directory,
        config.copy
        )

if __name__ == "__main__":
    main()