import json
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound

from core.models import UserTag

@login_required
def profile_tag_delete(request, tag_id):
    if request.method == "POST":
        tag = get_object_or_404(ProfileTag, pk=tag_id)

        request.user.get_profile().tags.remove(tag)
        request.user.get_profile().save()

        return HttpResponse(json.dumps({}), content_type="application/json")
    else:
        return HttpResponseNotFound()
