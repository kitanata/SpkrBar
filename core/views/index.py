import json
import random
from datetime import datetime, timedelta

from core.helpers import template

from talks.models import Talk
from talks.serializers import TalkSerializer
from rest_framework.renderers import JSONRenderer

@template('index.haml')
def index(request):
    talks = Talk.objects.filter(published=True).order_by('updated_at')[:12]
    talks = JSONRenderer().render(TalkSerializer(talks).data)

    return {'talks': talks}
