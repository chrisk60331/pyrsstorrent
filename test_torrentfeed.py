from unittest.mock import Mock, patch

import pendulum

from constants import DATETIME_FORMAT
from torrentfeed import TorrentFeed


def test_torrent_feed():
    mock_entry = Mock(published=pendulum.now().strftime(DATETIME_FORMAT))
    expected = [mock_entry]
    news_feed = Mock(entries=[mock_entry])

    actual = TorrentFeed(news_feed, pendulum.now().add(months=-1))

    assert actual.listings == expected
