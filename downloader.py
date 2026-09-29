# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:08:05 2026

@author: mark
"""

from pathlib import Path
import requests


class DownloadError(Exception):
    pass


class Downloader:

    def __init__(self, logger):

        self.logger = logger

    def download(
        self,
        url: str,
        destination: Path
    ) -> Path:
        """
        Download a file to the destination folder.

        Returns:
            Full path to the downloaded file.
        """

        destination.mkdir(parents=True, exist_ok=True)

        filename = url.split("/")[-1]

        output_file = destination / filename

        self.logger.info("")
        self.logger.info("Downloading")
        self.logger.info("-----------")
        self.logger.info(filename)

        response = requests.get(
            url,
            stream=True,
            timeout=60
        )

        if response.status_code != 200:
            raise DownloadError(
                f"HTTP {response.status_code}"
            )

        total_size = int(
            response.headers.get(
                "content-length",
                0
            )
        )

        downloaded = 0
        last_percent = -1

        with open(output_file, "wb") as f:

            for chunk in response.iter_content(
                chunk_size=1024 * 1024
            ):

                if not chunk:
                    continue

                f.write(chunk)

                downloaded += len(chunk)

                if total_size:

                    percent = int(
                        downloaded * 100 / total_size
                    )

                    if percent != last_percent:

                        self.logger.info(
                            f"{percent}%"
                        )

                        last_percent = percent

        self.logger.info("Download complete")

        return output_file