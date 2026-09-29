# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 20:10:35 2026

@author: mark
"""

from pathlib import Path
import subprocess
import ctypes


class ProcessError(Exception):
    pass


class ProcessRunner:

    def __init__(self, logger):
        self.logger = logger

    # ------------------------------------------------------------------
    # Run a normal process
    # ------------------------------------------------------------------

    def run(
        self,
        executable: Path,
        arguments: list[str] | None = None,
        working_directory: Path | None = None,
    ) -> int:

        if arguments is None:
            arguments = []

        command = [str(executable)] + arguments

        self.logger.info("")
        self.logger.info("Executing Process")
        self.logger.info("-----------------")
        self.logger.info(f"Executable : {executable}")
        self.logger.info(f"Arguments  : {' '.join(arguments)}")

        result = subprocess.run(
            command,
            cwd=working_directory,
        )

        return result.returncode

    # ------------------------------------------------------------------
    # Run with Administrator privileges
    # ------------------------------------------------------------------

    def run_as_admin(
        self,
        executable: Path,
        arguments: list[str] | None = None,
        working_directory: Path | None = None,
    ):

        if arguments is None:
            arguments = []

        self.logger.info("")
        self.logger.info("Launching Elevated Process")
        self.logger.info("--------------------------")
        self.logger.info(f"Executable : {executable}")
        self.logger.info(f"Arguments  : {' '.join(arguments)}")

        params = " ".join(arguments)

        result = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            str(executable),
            params,
            str(working_directory),
            1
        )

        #
        # Windows returns values <=32 on failure.
        #

        if result <= 32:

            raise ProcessError(
                f"ShellExecute failed ({result})"
            )

        self.logger.info("Process launched successfully.")