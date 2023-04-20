import logging
import os

import pendulum
from feedparser import FeedParserDict

from constants import LOG_LEVEL

logging.basicConfig(level=os.environ.get(LOG_LEVEL, logging.INFO))


class TorrentFeed:
    def __init__(self, news_feed: FeedParserDict, delta_datetime: pendulum.datetime):
        self.listings = sorted(
            {
                entry
                for entry in news_feed.entries
                if delta_datetime
                and pendulum.parse(entry.published, strict=False)
                > delta_datetime
            },
            key=lambda x: x.published_parsed,
        )
        logging.debug(self.listings)
