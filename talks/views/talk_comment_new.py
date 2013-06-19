from django.shortcuts import redirect, get_object_or_404

from core.models import UserProfile

def talk_comment_new(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    if talk.speaker == request.user.get_profile():
        return redirect('/talk/' + talk_id)

    if request.method == "POST":
        anon = get_object_or_404(UserProfile, user__username="anonymous")

        if request.user.is_anonymous():
            comment = TalkComment(
                    talk=talk,
                    reviewer=anon,
                    comment= request.POST['comment'])
        else:
            comment = TalkComment(
                    talk=talk,
                    reviewer=request.user.get_profile(),
                    comment= request.POST['comment'])

        comment.save()


    return redirect('/talk/' + talk_id)
