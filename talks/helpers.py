from datetime import datetime
from itertools import groupby

def group_talk_events_by_date(talks, reverse=False):
    talks = [{
        'month_num': k,
        'date': datetime(month=k[0], year=k[1], day=1).strftime("%B %Y"),
        'events': list(g)} for k, g in groupby(talks, key=lambda x: (x.date.month, x.date.year))]
    talks.sort(key=lambda x: x['month_num'], reverse=reverse)

    return talks
