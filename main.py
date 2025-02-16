from json import loads as json_loads
from os import getenv
from typing import Optional

from bs4 import ResultSet, Tag
from dotenv import load_dotenv

from HTML_rqs_resps import get_watchlist, parse_watchlist
from handle_csv import save_to_csv


def main() -> None:
    load_dotenv()
    usernames = getenv('USERNAMES')
    if usernames is None:
        return
    usernames = json_loads(usernames)
    if usernames is None:
        return

    total_movies = {}
    for i in range(len(usernames)):
        username = usernames[i]
        watchlist: Optional[ResultSet[Tag]] = get_watchlist(username)
        if watchlist is None:
            return

        movies = parse_watchlist(watchlist)
        total_movies[i] = movies

    intersection_movies = list(
        movie
        for movie in total_movies[0]
        if all(movie in total_movies[i] for i in range(1, len(total_movies)))
    )
    save_to_csv(intersection_movies, 'movies.csv')


if __name__ == '__main__':
    main()
