# Create your views here.
from django.db.models import Q

from core.helpers import template

from core.models import NormalUser

@template('speaker_list.haml')
def speaker_list(request):
    speakers = NormalUser.objects.all()[:20]

    return {'speakers': speakers }
