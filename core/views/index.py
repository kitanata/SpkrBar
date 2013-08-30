import random
from datetime import datetime, timedelta

from core.helpers import template

from talkevents.models import TalkEvent

@template('index.haml')
def index(request):
    talk_events = TalkEvent.objects.filter(talk__published=True)

    start_date = datetime.now()
    upcoming = talk_events.filter(date__gte=start_date
            ).order_by('date')[:4]

    past = talk_events.filter(date__lte=start_date
            ).order_by('-date')[:4]

    return {'upcoming': upcoming,
            'past': past}
