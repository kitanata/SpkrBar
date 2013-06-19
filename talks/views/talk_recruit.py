from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from events.models import Event

@login_required
def talk_recruit(request, talk_id):
    if request.method == "POST":
        if request.POST['event']:
            talk = get_object_or_404(Talk, pk=talk_id)
            event = get_object_or_404(Event, pk=request.POST['event'])

            submission = TalkEventSubmission()
            submission.talk = talk
            submission.event = event
            submission.event_accepts = True
            submission.save()

            Notification.create(talk.speaker, "<h2>An event invited you to speak.</h2>")

    if 'last' in request.GET and request.GET['last'] != '':
        return redirect(request.GET['last'])
    else:
        return redirect('/talk/' + talk_id)
