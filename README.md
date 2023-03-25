# Python RSS Torrent Feed
Get a feed of torrents. Use it to automate content retrieval, with transmission and showrss.info.
## Installation
```shell
pyenv python3 -m pip install -r requirements.txt
```
## Usage
```shell
echo "0 * * * * pyenv exec python main.py https://showrss.info/user/dsfnosdn.rss" > .torrenttask
crontab  .torrenttask
```
## Tests
```shell
pyenv pytest .
```