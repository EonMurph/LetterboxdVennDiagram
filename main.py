from json import loads as json_loads
from os import getenv
from typing import Optional

from bs4 import ResultSet, Tag
from dotenv import load_dotenv

from HTML_rqs_resps import get_watchlist, parse_watchlist


def main() -> None:
    load_dotenv()
    usernames = getenv('USERNAMES')
    if usernames is not None:
        username = json_loads(usernames)[0]

    watchlist: Optional[ResultSet[Tag]] = get_watchlist(username)
    if watchlist is None:
        return

    parse_watchlist(watchlist)


if __name__ == '__main__':
    main()
