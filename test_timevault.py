from unittest.mock import patch

import pendulum.parser

from constants import DATETIME_FORMAT
from timevault import TimeVault


def test_time_vault():
    expected = pendulum.now()

    with patch("timevault.TimeVault.state_file", "poop_file"):
        actual = TimeVault(expected).time.strftime(DATETIME_FORMAT)

    assert actual == expected.strftime(DATETIME_FORMAT)
