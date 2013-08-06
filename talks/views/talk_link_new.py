from urlparse import urlparse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound

from talks.models import Talk, TalkLink
from talks.forms import TalkLinkForm

@login_required
def talk_link_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('change_talk', talk):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TalkLinkForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']

            if not name:
                name = "Link"

            link = TalkLink()
            link.name = name
            link.url = urlparse(form.cleaned_data['url'], scheme="http"
                    ).geturl()
            link.talk = talk
            link.save()

            return redirect(talk)
        return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()
