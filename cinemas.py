import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta


def get_date_for_search():
    delta_days = 30
    start_day = datetime.now() - timedelta(days=delta_days)
    return start_day.date()


def fetch_afisha_page():
    url_afisha = 'https://www.afisha.ru/msk/schedule_cinema/'
    raw_html = requests.get(url_afisha).content
    return raw_html


def parse_afisha_list(afisha_html):
    content = bs(afisha_html, 'html.parser')
    content_movies = content('div',
                             {'class': 'object s-votes-hover-area collapsed'})
    info_movies_afisha = []
    for movie in content_movies:
        title_movie = movie('h3', {'class': 'usetags'})[0].get_text()
        count_cinemas = len(movie('td',{'class': 'b-td-item'},'a'))
        dict_info_movies = {'title': title_movie,
                            'number_cinemas': count_cinemas}
        info_movies_afisha.append(dict_info_movies)
    return info_movies_afisha


def fetch_movie_info():
    url_kinopoisk_premier = 'https://www.kinopoisk.ru/premiere/ru/2017/month/{}/'.format(9)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36'
    }
    raw_html = requests.get(url_kinopoisk_premier).content
    return raw_html


def get_films_in_kinopoisk(kinopoisk_html, initial_date):
    content = bs(kinopoisk_html, 'html.parser')
    content_movies = content.find_all('div', {'class': 'premier_item'})
    info_movies_kinopoisk = []
    for item in content_movies:
        title = item.find('span').text
        start_date = item.find('meta').get('content')

        raiting = item.find('u').text.split()
        dict_info_movies = {'title': title,
                            'start_date': start_date,
                            'raiting':raiting[0]}
        start_date = datetime.strptime(start_date,"%Y-%m-%d").date()
        if start_date >= initial_date:
            info_movies_kinopoisk.append(dict_info_movies)
    print(info_movies_kinopoisk)





def output_movies_to_console(movies):
    pass


if __name__ == '__main__':
#    print(get_date_for_search())
#    afisha_html = fetch_afisha_page()
#    info_movies = parse_afisha_list(afisha_html)
    initial_date = get_date_for_search()
    kinopoisk_html = fetch_movie_info()
    get_films_in_kinopoisk(kinopoisk_html, initial_date)

