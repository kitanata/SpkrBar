import random
from datetime import datetime, timedelta

from talkevents.models import TalkEvent

def talk_event_groups(sample_size=0):
    group_defs = [ 
            ('-', 14, "In the past couple weeks"), 
            ('+', 7, "Upcoming this week"), 
            ('+', 30, "In the next 30 days"),
            ('+', 90, "In the next 3 months"), 
            ('+', 90, "In the next 6 months"), 
            ('+', 180, "In the next year") ]

    talk_events = TalkEvent.objects.filter(talk__published=True)

    groups = []
    end_date = datetime.today()
    for group in group_defs:
        if group[0] == '-':
            start_date = datetime.today() - timedelta(days=group[1])
            end_date = datetime.today()
        else:
            start_date = end_date
            end_date = start_date + timedelta(days=group[1])

        result = talk_events.filter(event__start_date__gt=start_date,
                event__start_date__lt=end_date)

        if sample_size and len(result) > sample_size:
            result = random.sample(result, sample_size)

        result = list(result)
        result.sort(key=lambda x: x.date)

        groups.append((group[2], result))

    return groups
