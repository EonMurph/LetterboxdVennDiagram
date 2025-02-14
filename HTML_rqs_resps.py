from typing import Optional

from bs4 import BeautifulSoup, ResultSet, Tag
from requests import Response, exceptions, get


def get_watchlist(username: str) -> Optional[ResultSet[Tag]]:
    URL = f'https://letterboxd.com/{username}/watchlist/'
    try:
        response: Response = get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        movies: ResultSet[Tag] = soup.find_all(
            'li', {'class': 'poster-container'}
        )
        if movies is None:
            print('No poster list found.')
        return movies

    except exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return None


def parse_watchlist(watchlist: ResultSet[Tag]):
    for movie in watchlist:
        movie = movie.find('div')
        movie_title: str = movie['data-film-slug']
        print(movie_title)
