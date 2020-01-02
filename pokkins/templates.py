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
