from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound

@login_required
def talk_link_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if not request.user.has_perm('change_talk', talk):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TalkLinkForm(request.POST)

        if form.is_valid():
            link = TalkLink()
            link.name = form.cleaned_data['name']
            link.url = form.cleaned_data['url']
            link.talk = talk
            link.save()

            return redirect(talk)
    else:
        return HttpResponseNotFound()
