import random
from datetime import datetime, timedelta

from core.helpers import template

from models import TalkEvent

@template("talkevent_list.haml")
def talk_event_list(request):
    group_defs = [ 
            ('-', 14, "In the past couple weeks"), 
            ('+', 7, "Upcoming this week"), 
            ('+', 30, "In the next 30 days"),
            ('+', 90, "In the next 3 months"), 
            ('+', 90, "In the next 6 months"), 
            ('+', 180, "In the next year") ]

    talk_events = TalkEvent.objects.filter(
            event__owner__published=True,
            talk__published=True,
            talk__speaker__published=True)

    user_events = None
    if not request.user.is_anonymous():
        user_events = request.user.get_profile().event_set.all()

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

        if len(result) > 9:
            result = random.sample(result, 8)

        result = list(result)
        result.sort(key=lambda x: x.date)

        groups.append((group[2], result))

    return {
        'user_events': user_events,
        'talk_groups': groups }
