# Create your views here.
from django.db.models import Q, Count

from core.helpers import template

from core.models import SpkrbarUser

@template('speaker_list.haml')
def speaker_list(request):
    speakers = SpkrbarUser.objects.all().annotate(
            num_tags=Count('tags'),
            num_links=Count('links')).order_by(
                    '-photo', '-about_me', '-num_tags', '-num_links')[:20]

    return {
            'speakers': speakers,
            'last': '/speakers' }
