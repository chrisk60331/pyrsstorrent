import logging

from feedparser import FeedParserDict

from timevault import TimeVault
import pendulum
logging.basicConfig(level=logging.INFO)


class TorrentFeed:

    def __init__(self, news_feed: FeedParserDict, time_vault: TimeVault):
        self.listings = sorted(
            {
                ent
                for ent in news_feed.entries
                if time_vault.time and pendulum.parse(ent.published, strict=False) > time_vault.time
            }, key=lambda x: x.published_parsed
        )
