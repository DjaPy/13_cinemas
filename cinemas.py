from collections import defaultdict
from datetime import datetime, timedelta
import re
import requests
from bs4 import BeautifulSoup as bs


def get_date_for_search():
    delta_days = 20
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
            info_movie = (title_movie, {'number_cinemas': count_cinemas})
            info_movies_afisha.append(info_movie)
    return info_movies_afisha


def fetch_movie_info(last_month, current_month):
    url_premiers_last = 'https://www.kinopoisk.ru/premiere/ru/2017/month/{}/'.format(last_month)
    url_premiers_current = 'https://www.kinopoisk.ru/premiere/ru/2017/month/{}/'.format(current_month)
    last_month_content = requests.get(url_premiers_last).content
    current_month_content = requests.get(url_premiers_current).content
    full_content = last_month_content + current_month_content
    return full_content


def get_films_in_kinopoisk(kinopoisk_content, initial_date, current_date):
    good_rate = 3.0
    content = bs(kinopoisk_content, 'html.parser')
    content_movies = content.find_all('div', {'class': 'premier_item'})
    info_movies_kinopoisk = []
    for movie in content_movies:
        title = movie.find('span').text
        start_date = movie.find('meta').get('content')
        rating = movie.find('u').text.split()[0]
        if re.search('\W.',rating) is None:
            rating = '0'
        start_date = datetime.strptime(start_date,"%Y-%m-%d").date()
        if current_date >= start_date >= initial_date and float(rating) >= good_rate:
            info_movie = (title, {'rating' : rating})
            info_movies_kinopoisk.append(info_movie)
    return info_movies_kinopoisk


def get_pop_movies(list_afisha, list_kinopoisk):
    common_title_list = list_afisha + list_kinopoisk
    common_info_list = defaultdict(list)
    for title, info_movie in common_title_list:
        common_info_list[title].append(info_movie)
    common_info_list = sorted(common_info_list.items())
    return common_info_list


def get_preform(movies):
    count_of_information_units = 2
    output_list_films = []
    for film in movies:
        title_film, info_about_film = film
        if len(info_about_film) == count_of_information_units:
            count_cinemas = info_about_film[0]
            rate = info_about_film[1]
            output_dict_film = {}
            output_dict_film.update(count_cinemas)
            output_dict_film.update(rate)
            output_dict_film.update(title_film=title_film)
            output_list_films.append(output_dict_film)
    return output_list_films


def output_movies_to_console(output_list):
    for film in output_list[:10]:
        movie = 'Film: {}'.format(film['title_film'])
        rate = 'Kinopoisk rating: {}'.format(film['rating'])
        count_cinemas = 'Show in {} cinemas in Moscow'.format(film['number_cinemas'])
        print(movie)
        print(rate)
        print(count_cinemas + '\n')


if __name__ == '__main__':

    current_date, initial_date = get_date_for_search()
    current_month = datetime.today().month
    last_month = current_month - 1
    kinopoisk_content = fetch_movie_info(last_month,current_month)
    list_kinopoisk = get_films_in_kinopoisk(kinopoisk_content, initial_date, current_date)
    afisha_content = fetch_afisha_page()
    list_afisha = parse_afisha_list(afisha_content)
    movies = get_pop_movies(list_afisha, list_kinopoisk)
    output_list = get_preform(movies)
    output_movies_to_console(output_list)