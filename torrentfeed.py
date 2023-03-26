import logging

import pendulum
from feedparser import FeedParserDict


logging.basicConfig(level=logging.INFO)


class TorrentFeed:
    def __init__(self, news_feed: FeedParserDict, delta_datetime: pendulum.datetime):
        self.listings = sorted(
            {
                ent
                for ent in news_feed.entries
                if delta_datetime
                and pendulum.parse(ent.published, strict=False)
                > delta_datetime
            },
            key=lambda x: x.published_parsed,
        )
