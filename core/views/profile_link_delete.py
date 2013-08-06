import json
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden

from core.models import UserLink

@login_required
def profile_link_delete(request, link_id):
    if request.method == "POST":
        link = get_object_or_404(UserLink, pk=link_id)

        if link.user != request.user:
            return HttpResponseForbidden()

        link.delete()

        return HttpResponse(json.dumps({}), content_type="application/json")
    else:
        return HttpResponseNotFound()
