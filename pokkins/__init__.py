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

__version__ = "0.1.0"

DEFAULT_OWNER_NAME = "Pokkins Podcast Service"
DEFAULT_OWNER_EMAIL = "pokkins@matelsky.com"
DEFAULT_DURATION = 153_762

EPISODE_TEMPLATE = """
<item>
    <title>{title}</title>
    <description>{description}</description>
    <itunes:summary>{description}</itunes:summary>
    <itunes:subtitle>{description}</itunes:subtitle>
    <itunesu:category itunesu:code="112" />
    <enclosure url="{filepath}" type="audio/mpeg" length="1" />
    <guid>{filepath}</guid>
    <itunes:duration>{duration}</itunes:duration>
    <pubDate>{published_date}</pubDate>
</item>
"""

RSS_TEMPLATE = """
<?xml version="1.0" encoding="utf-8"?>
<rss xmlns:atom="http://www.w3.org/2005/Atom"
    xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
    xmlns:itunesu="http://www.itunesu.com/feed" version="2.0">
    <channel>
        <link>{root_url}</link>
        <language>en-us</language>
        <copyright>{current_year}</copyright>
        <webMaster>{owner_email} ({owner_name})</webMaster>
        <managingEditor>{owner_email} ({owner_name})</managingEditor>
        <image>
            <url>{image_url}</url>
            <title>pokkins icon</title>
            <link>{root_url}</link>
        </image>
        <itunes:owner>
            <itunes:name>{owner_name}</itunes:name>
            <itunes:email>{owner_email}</itunes:email>
        </itunes:owner>
        <itunes:category text="Education">
            <itunes:category text="Higher Education" />
        </itunes:category>
        <itunes:keywords>pokkins, audio</itunes:keywords>
        <itunes:explicit>no</itunes:explicit>
        <itunes:image href="{image_url}" />
        <atom:link href="{root_url}/feed.xml" rel="self" type="application/rss+xml" />
        <pubDate>{created_date}</pubDate>
        <title>{title}</title>
        <itunes:author>{owner_name}</itunes:author>
        <description>{description}</description>
        <itunes:summary>{description}</itunes:summary>
        <itunes:subtitle>{description}</itunes:subtitle>
        <lastBuildDate>{build_date}</lastBuildDate>
        {episodes}
    </channel>
</rss>
"""


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
    ) -> None:
        """
        Create a new pokkins host for a podcast.

        The only required argument is `episode_filepath`. All other arguments
        may be omitted.
        """
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
