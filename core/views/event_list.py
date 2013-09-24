from datetime import datetime, timedelta
from itertools import groupby
from django.db.models import Count

from core.helpers import template
from engagements.models import Engagement

@template('event_list.haml')
def event_list(request):
    start_date = datetime.today() - timedelta(days=14)
    end_date = datetime.today() + timedelta(days=14)

    engagements = Engagement.objects.filter(
        date__gte=start_date.date(), date__lt=end_date.date()
        ).order_by('event_name')

    events = list()
    for name, engs in groupby(engagements, key=lambda x: x.event_name):
        engs = list(engs)
        earliest_eng = min(map(lambda x: datetime.combine(x.date, x.time), engs))
        latest_eng = max(map(lambda x: datetime.combine(x.date, x.time), engs))
        tags = list(reduce(lambda x, y : x | y, map(lambda z: z.talk.tags.all(), engs)))
        tags = sorted([(tags.count(x), x.name) for x in set(tags)], key=lambda x: -x[0])
        events.append({
            'name': name,
            'numtalks': len(engs),
            'earliest_date': earliest_eng.date,
            'earliest_time': earliest_eng.time,
            'latest_date': latest_eng.date,
            'latest_time': latest_eng.time,
            'tags': tags,
        })

    events.sort(key=lambda x: -x['numtalks'])

    return {
        'events': events
    }
