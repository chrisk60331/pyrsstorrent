import logging
import os
import sys

import feedparser
import pendulum
import requests_html

from timevault import TimeVault
from torrentfeed import TorrentFeed

logging.basicConfig(level=logging.INFO)
DEFAULT_DATETIME = "Thu, 01 Jan 1970 00:00:01 +0000"
DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "Downloads")
RESET = os.environ.get("RESET", False)

if __name__ == "__main__":
    news_feed = feedparser.parse(sys.argv[1])
    time_vault = TimeVault()

    if RESET:
        time_vault.set(pendulum.parse(DEFAULT_DATETIME, strict=False))

    hashes = TorrentFeed(news_feed, time_vault.time)

    if hashes.listings:
        logging.info(f"found {len(hashes.listings)} new listings")
        for entry in hashes.listings:
            description = entry.description.replace("\\s", ".")[13:45].strip()
            torrent_path = os.path.join(
                os.path.expanduser("~"),
                DOWNLOAD_LOCATION,
                f"{description}.torrent",
            )

            logging.info(f"{entry.published} writing out {torrent_path}")
            torrent = requests_html.HTMLSession().get(url=entry.link)

            if torrent.status_code == 200:
                with open(torrent_path, "wb") as torrent_file:
                    torrent_file.write(torrent.content)

        time_vault.set(
            pendulum.parse(hashes.listings[-1].published, strict=False)
        )
