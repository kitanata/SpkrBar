# Create your views here.
from django.db.models import Q, Count

from core.helpers import template

from core.models import SpkrbarUser
from core.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer

@template('speaker_list.haml')
def speaker_list(request):
    speakers = SpkrbarUser.objects.all().annotate(
            num_tags=Count('tags'),
            num_links=Count('links')).order_by(
                    '-photo', '-about_me', '-num_tags', '-num_links')[:20]

    speakers = JSONRenderer().render(UserSerializer(speakers, many=True).data)
    
    return {'speakers': speakers, 'title': "Featured Speakers"}
