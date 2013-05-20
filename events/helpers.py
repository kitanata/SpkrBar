from datetime import datetime
from itertools import groupby

def group_events_by_date(talks, reverse=False):
    talks = [{
        'month_num': k,
        'date': datetime(month=k[1], year=k[0], day=1).strftime("%B %Y"),
        'events': list(g)} for k, g in groupby(talks, key=lambda x: (x.date.year, x.date.month))]

    talks.sort(key=lambda x: x['month_num'], reverse=reverse)
    return talks
