from datetime import datetime, timedelta

from django.db.models import Q

from core.helpers import render_to

from events.models import Event

def event_list(request):
    if request.user.is_anonymous():
        events = Event.objects.filter(owner__published=True)
    else:
        events = Event.objects.filter(
                Q(owner__published=True) | Q(owner=request.user))

    group_defs = [ 
            ('-', 30, "Recent Events"), 
            ('+', 14, "Upcoming Events"), 
            ('+', 90, "In the next 3 months"),
            ('+', 270, "In the next year")]

    groups = []
    end_date = datetime.today()
    for group in group_defs:
        if group[0] == '-':
            start_date = datetime.today() - timedelta(days=group[1])
            end_date = datetime.today()
        else:
            start_date = end_date
            end_date = start_date + timedelta(days=group[1])

        result = events.filter(start_date__gt=start_date,
                start_date__lt=end_date)

        if len(result) > 9:
            result = random.sample(result, 8)

        result = list(result)
        result.sort(key=lambda x: x.start_date)

        groups.append((group[2], result))

    return render_to(request, 'events/event_list.haml', context={'event_groups': groups})
