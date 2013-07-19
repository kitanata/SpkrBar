from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound

from talks.models import Talk
from talks.forms import TalkForm

@login_required
def talk_edit(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('change_talk', talk):
        return HttpResponseForbidden()

    if request.method == 'POST': # If the form has been submitted...
        form = TalkForm(request.POST, instance=talk)

        if form.is_valid():
            form.save()

            return redirect(talk)
    else:
        return HttpResponseNotFound()
