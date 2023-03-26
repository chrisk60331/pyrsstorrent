from unittest.mock import Mock, patch

import pendulum

from constants import DATETIME_FORMAT
from torrentfeed import TorrentFeed


def test_torrent_feed():
    mock_entry = Mock(published=pendulum.now().strftime(DATETIME_FORMAT))
    expected = [mock_entry]
    news_feed = Mock(entries=[mock_entry])
    time_vault = Mock()
    time_vault.time = pendulum.now().add(days=-1)

    with patch("timevault.TimeVault.state_file", "poop_file"):
        actual = TorrentFeed(news_feed, time_vault)

    assert actual.listings == expected
