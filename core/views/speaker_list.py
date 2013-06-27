# Create your views here.
from django.db.models import Q

from core.helpers import template

from core.models import NormalUser

@template('speaker_list.haml')
def speaker_list(request):
    if request.user.is_anonymous():
        speakers = NormalUser.objects.filter(Q(published=True))[:20]
    else:
        speakers = NormalUser.objects.filter(Q(published=True) | Q(user=request.user))[:20]

    return {'speakers': speakers }
