# Nutrition Mate

Nutrition-mate is a web application for tracking daily calories, macro nutrients, and measurements such as weight.

## Features

- Track daily calories
- Track daily weight and measurements
- Group foods in meals for easier tracking (WIP)
- Automatically add foods from the USDA database
- Calculate TDEE and daily nutrition targets
- Nutrition and weight analytics and visualizations (WIP)
- API for programmatic interaction (WIP)

## Technical Details

Nutrition-mate is a Flask web application backed by a mySQL database. As of the moment the front end is pure Flask and Bootstrap with no extra javascript or frameworks.

I have an instance running at [nutrition-mate.com](https://nutrition-mate.com). If you would like a registration key, email me at maxtrussell@gmail.com. No promises I can give one to everybody though, as it is currently running an a GCP f1-micro instance (with 0.6 GB memory).

### Install Guide

I'm working on a docker-compose for nutrition-mate, but in the meantime:

1. Clone repo (and cd into directory)

```bash
$ git clone git@github.com:maxtrussell/nutrition-mate.git
$ cd nutrition-mate
```

2. Install dependencies. If you're running MacOS use brew instead. If you're running Windows, you probably know better than I do.

```bash
$ sudo apt install python3.7
$ sudo apt install python3.7-venv
$ sudo apt install mysql-server
```

3. Setup mysql database. You can see the script in nutrition-mate/scripts/setup.sql.

```bash
$ sudo mysql
mysql> source scripts/setup.sql
```

4. Create python virtual environment

```bash
$ python3.7 -m venv env
$ source env/bin/activate
```

5. Install python requirements

```bash
$ pip install -r requirements.txt
```

6. Run server

```bash
$ python server.py
```

7. In another terminal test nutrition-mate

```bash
$ curl localhost:5000
```

8. (optional) To seed your admin database with 'verified foods'

```bash
$ python scripts/seed_foods.py -f data/verified_foods.json --username admin --endpoint localhost:5000/food
```

## Screenshots

![Log Page](https://storage.googleapis.com/nm-screenshots/nm-log.png "Log Page")
![Database Page](https://storage.googleapis.com/nm-screenshots/nm-db.png "Database Page")
![Weight Page](https://storage.googleapis.com/nm-screenshots/nm-weight.png "Weight Page")
![Weight Analytics](https://storage.googleapis.com/nm-screenshots/nm-weight-analytics.png "Weight Analytics")

