from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def talk_delete(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('delete_talk', talk):
        return HttpResponseForbidden()

    talk.delete()

    return redirect(request.user.get_profile())
