from datetime import datetime, timedelta

from django.db.models import Q

from core.helpers import render_to

from events.models import Event

def event_list(request):
    events = Event.objects.all()

    group_defs = [ 
            ('+', 0, 14, "Upcoming Events"), 
            ('-', 0, 30, "Recent Events"), 
            ('-', 30, 330, "Past Events"), 
            ('+', 30, 90, "In the next 3 months"),
            ('+', 90, 270, "In the next year")]

    groups = []
    today = datetime.today()
    for group in group_defs:
        if group[0] == '-':
            start_date = today - timedelta(days=group[2])
            end_date = today - timedelta(days=group[1])
        else:
            start_date = today + timedelta(days=group[1])
            end_date = today + timedelta(days=group[2])

        result = events.filter(start_date__gt=start_date,
                start_date__lt=end_date)

        if len(result) > 9:
            result = random.sample(result, 8)

        result = list(result)
        result.sort(key=lambda x: x.start_date)

        groups.append((group[3], result))

    return render_to(request, 'events/event_list.haml', context={'event_groups': groups})
