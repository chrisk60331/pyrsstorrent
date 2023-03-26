import json
import os
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path

import pendulum

from constants import DATETIME_FORMAT, READ, WRITE

STATE_FILE = ".last_tv_info_time"


class TimeVault:
    state_file = os.path.join(Path.home(), STATE_FILE)

    def __init__(self, init_time=None):
        if init_time:
            self.set(init_time)

        self.time = self.get()

    def get(self):
        try:
            return pendulum.parse(
                json.loads(open(self.state_file, mode=READ).read()),
                strict=False,
            )
        except (FileNotFoundError, JSONDecodeError):
            self.set(datetime.now())

    def set(self, new_time: datetime):
        self.time = new_time
        return open(self.state_file, mode=WRITE).write(
            json.dumps(self.time.strftime(DATETIME_FORMAT))
        )
