import json
from urlparse import urlparse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound

from talks.models import Talk, TalkLink
from talks.forms import TalkLinkForm

@login_required
def talk_link_delete(request, talk_id, link_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('change_talk', talk):
        return HttpResponseForbidden()

    if request.method == 'POST':
        link = get_object_or_404(TalkLink, pk=link_id)
        
        if talk != link.talk:
            return HttpResponseForbidden()

        link.delete()

        return HttpResponse(json.dumps({}), content_type="application/json")
    else:
        return HttpResponseNotFound()
