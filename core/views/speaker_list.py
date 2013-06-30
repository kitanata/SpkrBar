# Create your views here.
from django.db.models import Q

from core.helpers import template

from core.models import SpeakerProfile

@template('speaker_list.haml')
def speaker_list(request):
    speakers = SpeakerProfile.objects.all()[:20]

    return {'speakers': speakers }
