from django.shortcuts import redirect, get_object_or_404

from core.models import UserProfile
from talks.models import Talk, TalkComment

def talk_comment_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if talk.speaker == request.user.get_profile():
        return redirect('/talk/' + talk_id)

    if request.method == "POST":
        if not request.user.is_anonymous():
            comment = TalkComment(
                    talk=talk,
                    reviewer=request.user.get_profile(),
                    comment= request.POST['comment'])

        comment.save()


    return redirect('/talk/' + talk_id)
