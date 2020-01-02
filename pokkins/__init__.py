"""
pokkins

zero-config podcast audio hosting
"""
from typing import List

import datetime
import glob
import time
import os.path
from email.utils import formatdate  # RFC 2822 date formatting

from .templates import RSS_TEMPLATE, EPISODE_TEMPLATE
from .ip import get_global_ip

__version__ = "0.1.0"

DEFAULT_OWNER_NAME = "Pokkins Podcast Service"
DEFAULT_OWNER_EMAIL = "pokkins@matelsky.com"
DEFAULT_DURATION = 153_762


def format_date(date: float = None) -> str:
    if date is None:
        return formatdate()
    return formatdate(date)


def format_duration(duration_seconds: float) -> str:
    """
    H:MM:SS
    """
    h = duration_seconds // (60 * 60)
    m = (duration_seconds // 60) % 60
    s = duration_seconds % 60
    return f"{h}:{m}:{s}"


class Pokkins:
    def __init__(
        self,
        episode_filepath: str,
        title: str = None,
        description: str = None,
        owner_name: str = None,
        owner_email: str = None,
        host_address: str = None,
    ) -> None:
        """
        Create a new pokkins host for a podcast.

        The only required argument is `episode_filepath`. All other arguments
        may be omitted.
        """
        if host_address is None:
            self.host_address = get_global_ip() + ":8080"
        elif host_address.startswith(":"):
            self.host_address = get_global_ip() + host_address
        else:
            self.host_address = host_address

        self.episode_filepath = episode_filepath.rstrip("/") + "/"
        self.title = title if title else os.path.dirname(self.episode_filepath)
        self.description = (
            description
            if description
            else f"Automatically generated podcast using pokkins v{__version__}"
        )
        self.owner_name = owner_name if owner_name else DEFAULT_OWNER_NAME
        self.owner_email = owner_email if owner_email else DEFAULT_OWNER_EMAIL

        self.root_url = "http://localhost:8092"

    def generate_rss(self) -> str:
        now = format_date()
        return RSS_TEMPLATE.format(
            title=self.title,
            description=self.description,
            build_date=now,
            created_date=now,
            current_year=datetime.datetime.now().year,
            image_url="",
            owner_email=self.owner_email,
            owner_name=self.owner_name,
            root_url=self.root_url,
            episodes="\n".join(
                self._generate_episode_rss(f, order=i)
                for i, f in enumerate(self.get_episode_files())
            ),
        ).strip()

    def get_episode_files(self) -> List[str]:
        return [i.strip("/") for i in sorted(glob.glob(self.episode_filepath + "/**"))]

    def _generate_episode_rss(self, episode_filepath: str, order: int = 0) -> str:
        now = format_date(time.time() + order)
        fname = os.path.basename(episode_filepath)
        return EPISODE_TEMPLATE.format(
            title=fname,
            description=fname,
            filepath="{}/{}/{}".format(self.root_url, self.episode_filepath, fname),
            duration=format_duration(DEFAULT_DURATION),
            published_date=now,
        )
