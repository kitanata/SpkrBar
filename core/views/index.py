import random
from datetime import datetime, timedelta

from core.helpers import template

from talks.models import Talk

@template('index.haml')
def index(request):
    talks = Talk.objects.filter(published=True).order_by('updated_at')[:12]

    return {'talks': talks}
