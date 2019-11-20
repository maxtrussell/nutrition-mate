# Nutrition Mate

Nutrition-mate is a web application for tracking daily calories, macro nutrients, and measurements such as weight.

## Features

- Track daily calories
- Track daily weight and measurements
- Group foods in meals for easier tracking (WIP)
- Automatically add foods from the USDA database
- Calculate TDEE and daily nutrition targets

## Screenshots

![Log Page](https://storage.googleapis.com/nm-screenshots/nm-log.png "Log Page")
![Database Page](https://storage.googleapis.com/nm-screenshots/nm-db.png "Database Page")
![Weight Page](https://storage.googleapis.com/nm-screenshots/nm-weight.png "Weight Page")

## Technical Details

Nutrition-mate is a Flask web application backed by a mySQL database. As of the moment the front end is pure Flask and Bootstrap with no extra javascript or frameworks.

I have an instance running at [https://nutrition-mate.com]. If you would like a registration key, email me at maxtrussell@gmail.com. No promises I can give one to everybody though, as it is currently running an a GCP f1-micro instance (with 0.6 GB memory).

### Install Guide

I'm working on a docker-compose for nutrition-mate, but to run locally, in the meantime:

1. Clone repo (and cd into directory)

```
git clone git@github.com:maxtrussell/nutrition-mate.git
cd nutrition-mate
```

2. Install dependencies

```
$ sudo apt install python3.7
$ sudo apt install python3.7-venv
$ sudo apt install mysql-server
```

3. Setup mysql database

```
$ sudo mysql
mysql> source scripts/setup.sql
```

4. Create python virtual environment

```
$ python3.7 -m venv env
```

5. Install python requirements

```
$ pip install -r requirements.txt
```

6. Run server

```
$ python server.py
```

7. In another tab test nutrition-mate

```
$ curl localhost:5000
```

