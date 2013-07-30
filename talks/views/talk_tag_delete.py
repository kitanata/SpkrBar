import json
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound

from talks.models import Talk, TalkTag

@login_required
def talk_tag_delete(request, talk_id, tag_id):
    if request.method == "POST":
        talk = get_object_or_404(Talk, pk=talk_id)

        if not request.user.has_perm('change_talk', talk):
            return HttpResponseForbidden()

        tag = get_object_or_404(TalkTag, pk=tag_id)

        talk.tags.remove(tag)
        talk.save()

        return HttpResponse(json.dumps({}), content_type="application/json")
    else:
        return HttpResponseNotFound()
