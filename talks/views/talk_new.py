from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

from guardian.shortcuts import assign

from talks.models import Talk
from talks.forms import TalkForm

@login_required
def talk_new(request):
    if request.method == 'POST': # If the form has been submitted...
        talk_form = TalkForm(request.POST, request.FILES)
        location_form = None

        if talk_form.is_valid():
            talk = Talk()
            talk.name = talk_form.cleaned_data['name']
            talk.abstract = talk_form.cleaned_data['abstract']
            talk.speaker = request.user

            talk.save()
            assign('change_talk', request.user, talk)
            assign('delete_talk', request.user, talk)

            return redirect('/talk/' + str(talk.id))

    return HttpResponseNotFound()
