from typing import Optional
from re import search, sub

from bs4 import BeautifulSoup, ResultSet, Tag
from requests import Response, exceptions, get


def get_watchlist(username: str) -> list[Tag]:
    watchlist: list[Tag] = []
    URL = f'https://letterboxd.com/{username}/watchlist/'
    try:
        response: Response = get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        pages: Tag = soup.find('div', {'class': 'paginate-pages'})
        num_pages: int = int(pages.find_all('a')[-1].text)
        for i in range(1, num_pages + 1):
            print(i)
            URL = f'https://letterboxd.com/{username}/watchlist/page/{i}'
            response = get(URL)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            movies: ResultSet[Tag] = soup.find_all('li', {'class': 'poster-container'})
            if movies is None:
                print('No poster list found.')
            else:
                watchlist += [movie for movie in movies]

        return watchlist

    except exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return watchlist


def parse_watchlist(watchlist: list[Tag]) -> list[list[Optional[str]]]:
    movies: list[list[Optional[str]]] = []
    print(len(watchlist))
    for movie in watchlist:
        movie = movie.find('div')
        movie_title: str = movie['data-film-slug']
        URL = f'https://letterboxd/film/{movie_title}'
        movie_title = movie_title.replace('-', ' ')
        movie_title = sub(r'((mrs)|(mr)|(vs))', r'\1.', movie_title)
        year_search = search(r'[\d]{4}$', movie_title)
        if year_search is not None:
            year = year_search.group()
            movie_title = movie_title[:-5]
            movies.append([movie_title, year, URL])
        else:
            movies.append([movie_title, None, URL])

    return movies
