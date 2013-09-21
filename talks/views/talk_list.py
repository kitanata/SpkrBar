from datetime import datetime, timedelta
from engagements.models import Engagement

from core.helpers import template

@template('talks/talk_list.haml')
def talk_list(request):
    start_date = datetime.today() - timedelta(days=7)
    end_date = datetime.today()
    recent = Engagement.objects.filter(
        active=True, date__gte=start_date, date__lt=end_date
        ).order_by('-date', '-time')

    start_date = datetime.today()
    end_date = datetime.today() + timedelta(days=7)
    upcoming = Engagement.objects.filter(
        active=True, date__gte=start_date, date__lte=end_date
        ).order_by('-date', '-time')

    return {'upcoming': upcoming, 'recent': recent}
