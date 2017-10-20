import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import re


def get_date_for_search():
    delta_days = 30
    current_date = datetime.now().date()
    initial_date = (datetime.now() - timedelta(days=delta_days)).date()
    return  current_date, initial_date


def fetch_afisha_page():
    url_afisha = 'https://www.afisha.ru/msk/schedule_cinema/'
    raw_html = requests.get(url_afisha).content
    return raw_html


def parse_afisha_list(afisha_html):
    good_count_cinemas = 30
    content = bs(afisha_html, 'html.parser')
    content_movies = content('div',
                             {'class': 'object s-votes-hover-area collapsed'})
    info_movies_afisha = []
    for movie in content_movies:
        title_movie = movie('h3', {'class': 'usetags'})[0].get_text()
        count_cinemas = len(movie('td',{'class': 'b-td-item'},'a'))
        if int(count_cinemas) >= good_count_cinemas:
            dict_info_movies = {'title': title_movie,
                                'number_cinemas': count_cinemas}
            info_movies_afisha.append(dict_info_movies)
    return info_movies_afisha


def fetch_movie_info(last_month, current_month):
    url_premiers_last = 'https://www.kinopoisk.ru/premiere/ru/2017/month/{}/'.format(last_month)
    url_premiers_current = 'https://www.kinopoisk.ru/premiere/ru/2017/month/{}/'.format(current_month)
    last_month_content = requests.get(url_premiers_last).content
    current_month_content = requests.get(url_premiers_current).content
    full_content = last_month_content + current_month_content
    return full_content


def get_films_in_kinopoisk(kinopoisk_content, initial_date, current_date):
    good_rate = 7.0
    content = bs(kinopoisk_content, 'html.parser')
    content_movies = content.find_all('div', {'class': 'premier_item'})
    info_movies_kinopoisk = []
    for movie in content_movies:
        title = movie.find('span').text
        start_date = movie.find('meta').get('content')
        raiting = movie.find('u').text.split()[0]
        raiting = raiting.
        start_date = datetime.strptime(start_date,"%Y-%m-%d").date()
        if current_date >= start_date >= initial_date and float(raiting) >= good_rate:
            dict_info_movies = {'title': title,
                                'raiting': raiting}
            info_movies_kinopoisk.append(dict_info_movies)
    return info_movies_kinopoisk


def get_list_title(list):
    title_list = []
    for title in list:
        title = title.get('title')
        title_list.append(title)
    return title_list


def get_pop_movies(list_afisha, list_kinopoisk):
    title_list_afisha = get_list_title(list_afisha)
    title_list_kinopoisk = get_list_title(list_kinopoisk)
    common_list = list(set(title_list_afisha)&set(title_list_kinopoisk))
    return common_list


def output_movies_to_console(movies):
    pass


if __name__ == '__main__':
    current_date, initial_date = get_date_for_search()
    current_month = datetime.today().timetuple()[1]
    last_month = current_month - 1
    kinopoisk_content = fetch_movie_info(last_month,current_month)
    list_kinopoisk = get_films_in_kinopoisk(kinopoisk_content, initial_date, current_date)
    afisha_content = fetch_afisha_page()
    list_afisha = parse_afisha_list(afisha_content)
    print(get_pop_movies(list_afisha, list_kinopoisk))


