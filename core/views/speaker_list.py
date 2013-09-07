# Create your views here.
from django.db.models import Q, Count

from core.helpers import template

from core.models import SpeakerProfile

from talks.models import Talk

@template('speaker_list.haml')
def speaker_list(request):
    speakers = SpeakerProfile.objects.all().annotate(
            num_tags=Count('tags'),
            num_links=Count('user__links')).order_by(
                    '-photo', '-about_me', '-num_tags', '-num_links')
    talks_speakers = list(set(talk.speaker for talk in Talk.objects.all()))
    speakers = [spkr for spkr in speakers if spkr in talks_speakers][:20]
    return {
            'speakers': speakers,
            'last': '/speakers' }
