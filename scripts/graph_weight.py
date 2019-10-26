import argparse
from datetime import date, datetime
import json
import matplotlib.pyplot as plt
import numpy as np
import requests
import typing as t

ENDPOINT = 'http://nutrition-mate.com/api/weight?username={}'

def get_weights(username: str, start: date, end: date):
    r = requests.get(ENDPOINT.format(username))
    raw_weights = json.loads(r.content)
    weights = {}
    for date_str, weight in raw_weights.items():
        curr_date = parse_date(date_str)
        if curr_date >= start and curr_date < end:
            weights[curr_date] = weight
    return weights

def graph_weights(
    weights: t.Dict[date, float],
    start: date,
    end: date,
    regression: bool=False,
    stats: bool=False
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
    xvals, yvals = [], []
    for date, weight in weights.items():
        if date < start or date > end:
            continue
        days_elapsed = date - start_date
        xvals.append(days_elapsed.days)
        yvals.append(weight)
    plt.plot(xvals, yvals, 'b-')
    if regression:
        m,b = np.polyfit(xvals, yvals, 1)
        plt.plot(xvals, [m*x+b for x in xvals], 'r--')
        if stats:
            print(f'Regression: y = {m:.2f}x + {b:.2f}')

def stats(weights: t.Dict[str, float]):
    num_days = (max(weights.keys()) - min(weights.keys())).days
    w_max = max(weights.values())
    w_min = min(weights.values())
    w_range = w_max - w_min
    w_avg_change = 1.0 * w_range/num_days
    print(
        f'===== STATS ====\n'
        f'Total Days: {num_days}\n'
        f'Min: {w_min}, Max: {w_max}, Range: {w_range:.1f}\n'
        f'Avg Change per Day: {w_avg_change:.2f}'
    )

def parse_date(ds: str):
    return datetime.strptime(ds, '%Y-%m-%d').date()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, required=True)
    parser.add_argument('--start', type=str, default=None)
    parser.add_argument('--end', type=str, default=None)
    parser.add_argument('--regression', action='store_true')
    parser.add_argument('--stats', action='store_true')
    parser.add_argument('--graph', action='store_true')
    args = parser.parse_args()
    
    # set defaults for time range
    start = parse_date(args.start) if args.start else date()
    end = parse_date(args.end) if args.end else datetime.now().date()

    weights = get_weights(args.username, start, end)
    if args.stats:
        stats(weights)
    graph_weights(weights, start, end, regression=args.regression,
            stats=args.stats)
    if args.graph:
        plt.show()

if __name__ == '__main__':
    main()
