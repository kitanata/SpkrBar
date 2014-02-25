from datetime import datetime, timedelta

from engagements.models import Engagement
from engagements.serializers import EngagementSerializer
from rest_framework.renderers import JSONRenderer

from core.helpers import template

@template('talks/talk_list.haml')
def talk_list(request):
    start_date = datetime.today() - timedelta(days=180)
    end_date = datetime.today()
    recent = Engagement.objects.filter(
        date__gte=start_date, date__lt=end_date
        ).order_by('-date', '-time')

    start_date = datetime.today()
    end_date = datetime.today() + timedelta(days=90)
    upcoming = Engagement.objects.filter(
        date__gte=start_date, date__lte=end_date
        ).order_by('date', 'time')

    upcoming = JSONRenderer().render(EngagementSerializer(upcoming, many=True).data)
    recent = JSONRenderer().render(EngagementSerializer(recent, many=True).data)

    return {'upcoming': upcoming, 'recent': recent, 'title': "Recent Engagements"}
