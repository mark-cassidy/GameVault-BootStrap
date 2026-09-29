# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 15:53:05 2026

@author: mark
"""

import re
from dataclasses import dataclass

import requests


# Base URL for the GitHub REST API
GITHUB_API = "https://api.github.com"


# ----------------------------------------------------------------------
# Asset Object
# ----------------------------------------------------------------------

@dataclass
class GithubAsset:
    """
    Represents a downloadable file from a GitHub release.
    """

    name: str
    download_url: str
    size: int


# ----------------------------------------------------------------------
# Release Object
# ----------------------------------------------------------------------

@dataclass
class GithubRelease:
    """
    Represents the latest GitHub release.
    """

    tag: str
    name: str
    published: str
    assets: list[GithubAsset]


# ----------------------------------------------------------------------
# Exception
# ----------------------------------------------------------------------

class GithubError(Exception):
    pass


# ----------------------------------------------------------------------
# GitHub Client
# ----------------------------------------------------------------------

class GithubClient:

    def __init__(self, timeout=30):

        self.timeout = timeout

    def latest_release(self, repository: str) -> GithubRelease:
        """
        Download information about the latest release.
        """

        url = f"{GITHUB_API}/repos/{repository}/releases/latest"

        response = requests.get(url, timeout=self.timeout)

        if response.status_code != 200:
            raise GithubError(
                f"GitHub returned HTTP {response.status_code}"
            )

        data = response.json()

        assets = []

        for asset in data.get("assets", []):

            assets.append(
                GithubAsset(
                    name=asset["name"],
                    download_url=asset["browser_download_url"],
                    size=asset["size"]
                )
            )

        return GithubRelease(
            tag=data["tag_name"],
            name=data["name"],
            published=data["published_at"],
            assets=assets
        )

    def find_asset(
        self,
        release: GithubRelease,
        regex: str
    ) -> GithubAsset:
        """
        Search the release for an asset matching the supplied regex.
        """

        pattern = re.compile(regex)

        for asset in release.assets:

            if pattern.match(asset.name):
                return asset

        raise GithubError(
            f"No asset matched '{regex}'"
        )