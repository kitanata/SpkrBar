from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required()
def profile_archive(request):
    profile = request.user.get_profile()
    profile.published=False
    profile.save()

    return redirect('/speaker/' + request.user.username)
