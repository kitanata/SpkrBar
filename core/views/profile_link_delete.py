from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound

from core.models import UserLink

@login_required
def profile_link_delete(request, link_id):
    if request.method == "POST":
        link = get_object_or_404(UserLink, pk=link_id)
        link.delete()

        return redirect(request.user.get_absolute_url())
    else:
        return HttpResponseNotFound()
