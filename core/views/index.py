import random
from datetime import datetime, timedelta

from core.helpers import template

from talkevents.models import TalkEvent

@template('index.haml')
def index(request):
    talk_events = TalkEvent.objects.filter(talk__published=True)

    start_date = datetime.today() - timedelta(days=1)
    upcoming = talk_events.filter(event__start_date__gte=start_date
            ).order_by('date')[:20]

    past = talk_events.filter(event__end_date__lte=start_date
            ).order_by('date')[:20]

    if len(upcoming) > 4:
        upcoming = random.sample(upcoming, 4)

    if len(past) > 4:
        past = random.sample(past, 4)

    return {'upcoming': upcoming,
            'past': past}
