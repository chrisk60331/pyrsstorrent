import logging
import os
import sys
from datetime import datetime
import time

import feedparser
import pendulum
import requests_html

from constants import LOG_LEVEL
from timevault import TimeVault
from torrentfeed import TorrentFeed

logging.basicConfig(level=os.environ.get(LOG_LEVEL, logging.INFO))
DEFAULT_DATETIME = datetime.fromtimestamp(time.mktime(time.gmtime(0))).isoformat()
DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "Downloads")
RESET = os.environ.get("RESET", False)
TORRENT_FILE_SUFFIX = ".torrent"
MAGNET_FILE_SUFFIX = ".magnet"


def description_transform(in_description: str) -> str:
    trim_preamble = 13
    keep_desc_short = 55
    return in_description.replace(" ", ".")[
       trim_preamble:keep_desc_short
    ].strip()


if __name__ == "__main__":
    news_feed = feedparser.parse(sys.argv[1])
    time_vault = TimeVault()

    if RESET:
        time_vault.set(pendulum.parse(DEFAULT_DATETIME, strict=False))

    hashes = TorrentFeed(news_feed, time_vault.time)

    if hashes.listings:
        logging.info(f"found {len(hashes.listings)} new listings")
        for entry in hashes.listings:
            description = description_transform(entry.description)
            output_path = os.path.join(
                os.path.expanduser("~"),
                DOWNLOAD_LOCATION,
                description,
            )

            if entry.link.endswith(TORRENT_FILE_SUFFIX):
                torrent = requests_html.HTMLSession().get(url=entry.link).content.decode()
                output_path += TORRENT_FILE_SUFFIX
            else:
                torrent = entry.link
                output_path += MAGNET_FILE_SUFFIX

            logging.info(f"{entry.published} writing out {output_path}")

            with open(output_path, "w") as torrent_file:
                torrent_file.write(torrent)

        time_vault.set(
            pendulum.parse(hashes.listings[-1].published, strict=False)
        )
