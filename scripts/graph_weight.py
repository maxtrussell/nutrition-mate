import argparse
from datetime import date, datetime
from getpass import getpass
import json
import matplotlib.pyplot as plt
import numpy as np
import requests
import sys
import typing as t

ENDPOINT = 'https://nutrition-mate.com/api/weight'

def get_weights(username: str, start: date, end: date, local: bool=False):
    # 3 attempts to get password
    for i in range(3):
        password = getpass()
        r = requests.get(
            ENDPOINT.format(username),
            auth=requests.auth.HTTPBasicAuth(username, password),
        )
        if r.status_code != 401:
            break
        print('Sorry, try again.')
    r.raise_for_status()
    raw_weights = json.loads(r.content)
    weights = {}
    for date_str, weight in raw_weights.items():
        curr_date = parse_date(date_str)
        if curr_date >= start and curr_date <= end:
            weights[curr_date] = weight
    return weights

def graph_weights(
    weights: t.Dict[date, float],
    start: date,
    end: date,
    goal: float,
    ) -> None:
    """Plots weight in matplotlib

    Parameters:
    weights (t.Dict[str, float]): a dict mapping dates to weights
    start (date): the earliest date that will be plotted
    end (date): the lastest date that will be plotted
    regression (bool): whether to plot a regression line
    stats (bool): whether to print extra stats
    """
    start_date = datetime.now().date()
    for curr_date in weights:
        if curr_date < start_date:
            start_date = curr_date
    vals = []
    for date, weight in weights.items():
        days_elapsed = date - start_date
        vals.append((days_elapsed.days, weight))
    vals = sorted(vals, key=lambda x: x[0])
    xvals = [x[0] for x in vals]
    yvals = [y[1] for y in vals]
    plt.plot(xvals, yvals, 'b-', label='weight')
    if goal:
        m,b = goal/7, min(yvals)
        plt.plot(xvals, [m*x+b for x in xvals], 'g:', label='goal')
    n = 7
    plt.plot(xvals, rolling_avg(yvals, n), 'r--', label=f'{n} day avg')

    plt.xlabel(f'Days since {start_date}')
    plt.ylabel('Weight in pounds')
    plt.legend(loc='best')


def rolling_avg(vals: t.List[float], n: int=3):
    avgs = []
    for i, val in enumerate(vals):
        if i+1 < n:
            cumsum = sum(vals[:i+1])
            avgs.append(cumsum/(i+1))
        else:
            cumsum = sum(vals[(i+1)-n:i+1])
            avgs.append(cumsum/n)
    return avgs

def stats(weights: t.Dict[date, float]):
    first_date, last_date = min(weights.keys()), max(weights.keys())
    num_days = (last_date - first_date).days
    w_max = max(weights.values())
    w_min = min(weights.values())
    w_delta = weights[last_date] - weights[first_date]
    w_avg_change = 7.0 * w_delta/num_days
    print(
        f'===== STATS ====\n'
        f'Total Days: {num_days}\n'
        f'Min: {w_min}, Max: {w_max}, Delta: {w_delta:.1f}\n'
        f'Avg Change per week: {w_avg_change:.2f}\n'
    )

def report(weights: t.Dict[date, float], goal: float):
    start_date = min(weights.keys())
    curr_date = max(weights.keys())
    curr_day = (curr_date - start_date).days
    m, b = goal/7, weights[start_date]

    ideal_weight = m*curr_day + b
    predicted_day = (weights[curr_date] - weights[start_date]) / m

    print(
        f'===== REPORT =====\n'
        f'Current day: {curr_day}\n'
        f'Current weight: {weights[curr_date]}, Ideal weight: {ideal_weight:.1f}\n'
        f'You are {predicted_day - curr_day:.1f} day(s) off schedule.\n'
    )


def parse_date(ds: str):
    return datetime.strptime(ds, '%Y-%m-%d').date()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True)
    parser.add_argument('--start', default=None)
    parser.add_argument('--end', default=None)
    parser.add_argument('--goal', type=float, default=None)
    args = parser.parse_args()
    
    
    # set defaults for time range
    start = parse_date(args.start) if args.start else date(1, 1, 1)
    end = parse_date(args.end) if args.end else datetime.now().date()

    weights = get_weights(args.username, start, end)
    if len(weights) == 0:
        print(f'No weights found for period ({args.start}, {args.end})')
        sys.exit(0)
    stats(weights)
    graph_weights(weights, start, end, args.goal)
    if args.goal:
        report(weights, args.goal)
    plt.show()

if __name__ == '__main__':
    main()
