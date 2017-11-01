# Cinemas
The sripts selects 10 popular films that go to cinemas.

# How to intstall

Use Venv or virtualenv for insulation project. Virtualenv example:
```
$ python virtualevn myenv
$ source myenv/bin/activate
```

Install requirements:

```
pip install -r requirements.txt
```

If you have error, you need enter sudo before command.

# Quick launch


```
python cinemas.py
```

```
Film: Аритмия
Kinopoisk raiting: 7.99
Show in 82 cinemas in Moscow

Film: Бегущий по лезвию 2049
Kinopoisk raiting: 7.88
Show in 122 cinemas in Moscow

Film: Геошторм
Kinopoisk raiting: 5.91
Show in 149 cinemas in Moscow

Film: Голем
Kinopoisk raiting: 6.04
Show in 94 cinemas in Moscow

Film: Двуличный любовник
Kinopoisk raiting: 6.66
Show in 62 cinemas in Moscow

Film: Дом призраков
Kinopoisk raiting: 4.89
Show in 39 cinemas in Moscow

Film: Жизнь впереди
Kinopoisk raiting: 6.26
Show in 50 cinemas in Moscow

Film: Заклятье. Наши дни
Kinopoisk raiting: 4.98
Show in 61 cinemas in Moscow

Film: Между нами горы
Kinopoisk raiting: 6.64
Show in 37 cinemas in Moscow
```

# Settings for deep search

List of arguments:
- `-h, --help` - list of all commands;
- `-d, --day` - The number of days in cinemas;
- `-c, --count` - The number of cinemas which show the film;
- `-r, --rating` - Minimal movie rating;


**The initial settings.**

The data which are used, if you are added to the arguments when calling the script.
```
- day - 21
- count - 30
- rating - 3.00
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
