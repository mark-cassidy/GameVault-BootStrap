# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 20:02:24 2026

@author: mark
"""

from pathlib import Path

from config import InstallConfiguration
from process import ProcessRunner


class InstallerError(Exception):
    pass


class Installer:

    def __init__(self, logger):

        self.logger = logger
        self.process = ProcessRunner(logger)

    # ------------------------------------------------------------------

    def install(
        self,
        downloaded_file: Path,
        install_directory: Path,
        install_config: InstallConfiguration,
    ):

        install_type = install_config.type.lower()

        if install_type == "installer":

            self._install_exe(
                downloaded_file,
                install_directory,
                install_config,
            )

        elif install_type == "portable":

            self.logger.info("")
            self.logger.info("Portable installation not yet implemented.")

        else:

            raise InstallerError(
                f"Unknown install type '{install_type}'"
            )

    # ------------------------------------------------------------------

    def _install_exe(
        self,
        installer: Path,
        install_directory: Path,
        install_config: InstallConfiguration,
    ):

        self.logger.info("")
        self.logger.info("Running Installer")
        self.logger.info("-----------------")

        arguments = []

        #
        # Replace placeholders.
        #

        for arg in install_config.silent_args:

            arguments.append(
                arg.replace(
                    "{INSTALLDIR}",
                    str(install_directory)
                )
            )

        #
        # Launch the installer.
        #

        self.process.run_as_admin(
            executable=installer,
            arguments=arguments,
            working_directory=installer.parent
        )

        self.logger.info("")
        self.logger.info("Installer launched.")